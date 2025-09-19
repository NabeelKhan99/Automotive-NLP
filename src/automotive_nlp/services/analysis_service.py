import math
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from ..db import models
from ..nlp.preprocess import clean_text
from ..nlp.sentiment import analyze_sentiment

# --- Base repair costs (could be moved to config or DB later) ---
BASE_COSTS = {
    "brake": 200,
    "engine": 500,
    "ac": 300,
    "transmission": 700,
    "default": 250,
}

def estimate_cost(text: str, frequency: int, alpha: float = 0.1, cap: float = 0.5) -> float:
    """
    Estimate repair cost dynamically based on complaint frequency.

    Args:
        text (str): complaint text (used to infer base repair type).
        frequency (int): number of complaints in this cluster.
        alpha (float): sensitivity factor for price growth.
        cap (float): maximum percentage increase allowed (e.g., 0.5 = +50%).

    Returns:
        float: adjusted repair cost
    """
    # 1. Select base cost
    base_cost = BASE_COSTS["default"]
    for keyword, cost in BASE_COSTS.items():
        if keyword in text.lower():
            base_cost = cost
            break

    # 2. Dynamic adjustment with log growth
    adjusted = base_cost * (1 + alpha * math.log(1 + frequency))

    # 3. Apply cap
    max_allowed = base_cost * (1 + cap)
    final_cost = min(adjusted, max_allowed)

    return round(final_cost, 2)


def cluster_feedbacks_by_text(feedbacks: List[models.Feedback], n_clusters: int = 5) -> Dict[int, List[models.Feedback]]:
    """
    Cluster feedbacks by technical fault (unsupervised KMeans on cleaned text).
    """
    texts = [clean_text(f.text) for f in feedbacks]

    if len(texts) < n_clusters:
        n_clusters = max(1, len(texts))

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    clusters: Dict[int, List[models.Feedback]] = {}
    for feedback, label in zip(feedbacks, labels):
        clusters.setdefault(label, []).append(feedback)

    return clusters


def analyze_feedback(db: Session, cluster_by_make: bool = False, n_clusters: int = 5) -> List[Dict[str, Any]]:
    """
    Analyze stored feedbacks:
    - Cluster by faults (default) or car make/model
    - Compute sentiment
    - Suggest dynamic repair cost
    """
    feedbacks = db.query(models.Feedback).all()
    if not feedbacks:
        return []

    results = []

    if cluster_by_make:
        # Group by car make+model
        make_model_map: Dict[str, List[models.Feedback]] = {}
        for f in feedbacks:
            key = f"{f.car_make}_{f.car_model}"
            make_model_map.setdefault(key, []).append(f)

        for key, group in make_model_map.items():
            sentiments = [analyze_sentiment(f.text) for f in group]
            avg_sentiment = sum(sentiments) / len(sentiments)

            # Cost estimate from first complaint
            example_text = group[0].text
            suggested_cost = estimate_cost(example_text, len(group))

            results.append({
                "cluster": key,
                "count": len(group),
                "avg_sentiment": avg_sentiment,
                "suggested_cost": suggested_cost,
                "examples": [f.text for f in group[:3]],
            })
    else:
        # Cluster by fault
        clusters = cluster_feedbacks_by_text(feedbacks, n_clusters=n_clusters)
        for label, group in clusters.items():
            sentiments = [analyze_sentiment(f.text) for f in group]
            avg_sentiment = sum(sentiments) / len(sentiments)

            # Update DB
            for f in group:
                f.fault_cluster = f"cluster_{label}"
            db.commit()

            # Cost estimate from first complaint
            example_text = group[0].text
            suggested_cost = estimate_cost(example_text, len(group))

            results.append({
                "cluster": f"cluster_{label}",
                "count": len(group),
                "avg_sentiment": avg_sentiment,
                "suggested_cost": suggested_cost,
                "examples": [f.text for f in group[:3]],
            })

    return results

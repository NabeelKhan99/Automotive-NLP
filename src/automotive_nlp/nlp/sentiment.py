def analyze_sentiment(text: str) -> float:
    """
    Very simple heuristic sentiment:
     - positive keywords -> +0.9
     - negative keywords -> -0.9
     - else 0.0
    Replace with a proper model for production.
    """
    lower = (text or "").lower()
    positives = ["good", "great", "excellent", "perfect", "fine", "smooth", "works"]
    negatives = ["bad", "terrible", "broken", "noisy", "squeak", "squeaking", "rattle", "knock", "not working", "fail", "stalls", "grind"]

    if any(p in lower for p in positives):
        return 0.9
    if any(n in lower for n in negatives):
        return -0.9
    return 0.0

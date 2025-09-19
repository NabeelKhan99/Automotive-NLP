from sqlalchemy.orm import Session
from typing import List, Optional
from automotive_nlp.db import models, schemas

def save_feedback(db: Session, feedback_in: schemas.FeedbackCreate) -> models.Feedback:
    """
    Create a new Feedback object and add it to the session.
    Caller is responsible for committing and refreshing.
    """
    if not feedback_in.text.strip():
        raise ValueError("Feedback text cannot be empty")

    db_obj = models.Feedback(
        text=feedback_in.text.strip(),
        car_make=feedback_in.car_make.strip(),
        car_model=feedback_in.car_model.strip(),
    )
    db.add(db_obj)
    return db_obj   # <-- no flush/refresh, lifecycle handled by caller

def get_feedbacks(db: Session, skip: int = 0, limit: int = 100) -> List[models.Feedback]:
    return (
        db.query(models.Feedback)
        .order_by(models.Feedback.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def update_fault_cluster(db: Session, feedback_id: int, cluster_label: str) -> Optional[models.Feedback]:
    obj = db.get(models.Feedback, feedback_id)
    if not obj:
        return None
    obj.fault_cluster = cluster_label
    return obj   # caller decides when to commit

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from automotive_nlp.db.database import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    sentiment = Column(String, nullable=True)  # optional: precomputed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Vehicle info
    car_make = Column(String, nullable=False, index=True)    # e.g., "Toyota"
    car_model = Column(String, nullable=False, index=True)   # e.g., "Camry"

    # Fault categorization (can be updated later by clustering)
    fault_cluster = Column(String, nullable=True, index=True)

    def __repr__(self):
        return f"<Feedback id={self.id} make={self.car_make} model={self.car_model}>"

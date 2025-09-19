from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FeedbackBase(BaseModel):
    text: str
    car_make: str
    car_model: str

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackRead(FeedbackBase):
    id: int
    sentiment: Optional[str]
    fault_cluster: Optional[str]
    created_at: datetime

    # ✅ Pydantic v2 way to enable ORM mode
    model_config = {
        "from_attributes": True
    }

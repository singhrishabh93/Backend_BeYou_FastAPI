from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class AffirmationBase(BaseModel):
    text: str
    category: str

class AffirmationCreate(AffirmationBase):
    pass

class AffirmationInDB(AffirmationBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:10])
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class Affirmation(AffirmationInDB):
    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "a1b2c3d4e5",
                "text": "I am worthy of love and respect",
                "category": "self-esteem",
                "createdAt": "2023-03-01T12:00:00"
            }
        }
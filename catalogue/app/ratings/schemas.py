import uuid
from datetime import datetime
from typing import List, Optional
from app.general.utils.AllOptional import AllOptional
from pydantic import BaseModel, validator
from pydantic.typing import ForwardRef


class RatingBase(BaseModel):
    title: Optional[str]
    text: str
    value: int

    @validator('value')
    def value_not_greater_than_5(cls, v):
        if v > 5 or v < 0:
            raise ValueError('must be between 0 and 5')
        return v

class RatingCreate(RatingBase):
    artefact_id: uuid.UUID


class RatingPatch(RatingCreate, metaclass=AllOptional):
    pass


class Rating(RatingBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    user_id: str

    class Config:
        orm_mode = True


class RatingOut(Rating):
    pass
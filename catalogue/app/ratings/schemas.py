import uuid
from datetime import datetime
from typing import List, Optional
from app.general.utils.AllOptional import AllOptional
from pydantic import BaseModel, validator
from pydantic.typing import ForwardRef


class RatingBase(BaseModel):
    title: Optional[str]
    text: str


class RatingCreate(RatingBase):
    user_id: uuid.UUID
    artefact_id: uuid.UUID


class RatingPatch(RatingCreate, metaclass=AllOptional):
    pass


class Rating(RatingBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class RatingOut(Rating):
    pass
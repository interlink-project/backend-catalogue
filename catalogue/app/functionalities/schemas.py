import uuid
from datetime import datetime
from typing import List, Optional

from app.general.utils.AllOptional import AllOptional
from pydantic import BaseModel


class FunctionalityBase(BaseModel):
    name: str
    description: str


class FunctionalityCreate(FunctionalityBase):
    pass


class FunctionalityPatch(FunctionalityCreate, metaclass=AllOptional):
    pass


class Functionality(FunctionalityBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class FunctionalityOut(Functionality):
    pass

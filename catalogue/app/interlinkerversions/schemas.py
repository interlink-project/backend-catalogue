import uuid
from datetime import datetime
from typing import List, Optional

from app.general.utils.AllOptional import AllOptional
from pydantic import BaseModel

class InterlinkerVersionBase(BaseModel):
    description: str
    documentation: Optional[str]

class InterlinkerVersionCreate(InterlinkerVersionBase):
    backend: str
    init_asset_id: Optional[str]


class InterlinkerVersionPatch(InterlinkerVersionCreate, metaclass=AllOptional):
    pass


class InterlinkerVersionORM(InterlinkerVersionBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class InterlinkerVersionOut(InterlinkerVersionORM):
    backend: Optional[str]
    init_asset_id: Optional[str]

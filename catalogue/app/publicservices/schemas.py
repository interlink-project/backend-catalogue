import uuid
from datetime import datetime
from typing import List, Optional, Literal
from app.general.utils.AllOptional import AllOptional
from app.artefacts.schemas import (
    ArtefactBase,
    ArtefactCreate,
    ArtefactORM,
    ArtefactOut,
)


class PublicServiceBase(ArtefactBase):
    language: str
    processing_time: Optional[str]
    location: Optional[str]
    status: Optional[str]
    public_organization: Optional[str]
    output: Optional[str]
    cost: Optional[str]


class PublicServiceCreate(ArtefactCreate, PublicServiceBase):
    pass


class PublicServicePatch(PublicServiceCreate, metaclass=AllOptional):
    pass


class PublicServiceORM(ArtefactORM, PublicServiceBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class PublicServiceOut(ArtefactOut, PublicServiceORM):
    pass

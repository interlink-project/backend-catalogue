import uuid
from typing import List, Optional
from datetime import datetime

from app.general.db.base_class import Base as BaseModel
from pydantic import validator, BaseModel as PydanticBaseModel
from app.problemprofiles.schemas import ProblemProfileOut
from app.questioncomments.schemas import QuestionCommentOut

class ArtefactBase(PydanticBaseModel):
    name: str
    description: str
    logotype: Optional[str]
    published: Optional[bool]
    tags: str
    snapshots: Optional[List[str]]

class ArtefactCreate(ArtefactBase):
    problemprofiles: Optional[List[uuid.UUID]]


class ArtefactORM(ArtefactBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class ArtefactOut(ArtefactORM):
    artefact_type: str
    problemprofiles: List[ProblemProfileOut]

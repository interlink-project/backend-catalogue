import uuid
from typing import List, Optional
from datetime import datetime

from app.general.db.base_class import Base as BaseModel
from pydantic import BaseModel as PydanticBaseModel
from app.problemdomains.schemas import ProblemDomainOut
from app.questioncomments.schemas import QuestionCommentOut


class ArtefactBase(PydanticBaseModel):
    name: str
    description: str
    logotype: str
    published: bool
    keywords: List[str]


class ArtefactCreate(ArtefactBase):
    problemdomains: Optional[List[uuid.UUID]]
    functionalities: Optional[List[uuid.UUID]]


class ArtefactORM(ArtefactBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ArtefactOut(ArtefactORM):
    artefact_type: str
    problemdomains: List[ProblemDomainOut]

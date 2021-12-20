import uuid
from datetime import datetime
from typing import List, Optional

from app.general.utils.AllOptional import AllOptional
from pydantic import BaseModel
from app.functionalities.schemas import (
    FunctionalityBase,
    FunctionalityPatch,
    FunctionalityOut,
)


class ProblemDomainBase(BaseModel):
    name: str
    description: str
    functionalities: List[FunctionalityBase]
    target_stakeholder_groups: Optional[List[str]]


class ProblemDomainCreate(ProblemDomainBase):
    pass


class ProblemDomainPatch(ProblemDomainCreate, metaclass=AllOptional):
    functionalities: List[FunctionalityPatch]


class ProblemDomain(ProblemDomainBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ProblemDomainOut(ProblemDomain):
    functionalities: List[FunctionalityOut]

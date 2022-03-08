import uuid
from datetime import datetime
from typing import List, Optional
from app.general.utils.AllOptional import AllOptional
from pydantic import BaseModel, validator
from pydantic.typing import ForwardRef


class QuestionCommentBase(BaseModel):
    title: Optional[str]
    text: str


class QuestionCommentCreate(QuestionCommentBase):
    user_id: str
    artefact_id: Optional[uuid.UUID]
    parent_id: Optional[uuid.UUID]

    @validator("artefact_id", pre=True, always=True)
    def check_artefact_id_or_parent_id(cls, artefact_id, values):
        if not values.get("parent_id") and not artefact_id:
            raise ValueError("either artefact_id or parent_id is required")
        return artefact_id


class QuestionCommentPatch(QuestionCommentCreate, metaclass=AllOptional):
    pass


class QuestionComment(QuestionCommentBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class QuestionCommentOut(QuestionComment):
    children: Optional[ForwardRef("List[QuestionCommentOut]")]


QuestionCommentOut.update_forward_refs()

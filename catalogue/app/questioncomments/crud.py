

import uuid
from typing import List

from sqlalchemy.orm import Session

from app.models import QuestionComment
from app.schemas import QuestionCommentCreate, QuestionCommentPatch
from app.general.utils.CRUDBase import CRUDBase


class CRUDQuestionComment(CRUDBase[QuestionComment, QuestionCommentCreate, QuestionCommentPatch]):
    def get_multi_by_user(
        self, db: Session, *, user_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[QuestionComment]:
        return (
            db.query(self.model)
            .filter(QuestionComment.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_artefact(
        self, db: Session, *, artefact_id:  uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[QuestionComment]:
        return (
            db.query(self.model)
            .filter(QuestionComment.artefact_id == artefact_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, questioncomment: QuestionCommentCreate) -> QuestionComment:
        db_obj = QuestionComment(
            artefact_id=questioncomment.artefact_id,
            user_id=questioncomment.user_id,
            value=questioncomment.value,
            title=questioncomment.title,
            text=questioncomment.text,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


exportCrud = CRUDQuestionComment(QuestionComment)

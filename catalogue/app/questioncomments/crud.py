

import uuid
from typing import List

from sqlalchemy.orm import Session

from app.models import QuestionComment
from app.schemas import QuestionCommentCreate, QuestionCommentPatch
from app.general.utils.CRUDBase import CRUDBase


class CRUDQuestionComment(CRUDBase[QuestionComment, QuestionCommentCreate, QuestionCommentPatch]):
    async def get_multi_by_user(
        self, db: Session, user_id: str,
    ) -> List[QuestionComment]:
        return (
            db.query(self.model)
            .filter(QuestionComment.user_id == user_id)
            .all()
        )

    async def get_multi_by_artefact(
        self, db: Session, *, artefact_id: uuid.UUID,
    ) -> List[QuestionComment]:
        return (
            db.query(self.model)
            .filter(QuestionComment.artefact_id == artefact_id)
            .all()
        )

    async def create(self, db: Session, questioncomment: QuestionCommentCreate) -> QuestionComment:
        db_obj = QuestionComment(
            artefact_id=questioncomment.artefact_id,
            user_id=questioncomment.user_id,
            parent_id=questioncomment.parent_id,
            title=questioncomment.title,
            text=questioncomment.text,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


exportCrud = CRUDQuestionComment(QuestionComment)

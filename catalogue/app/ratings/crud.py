

import uuid
from typing import List

from sqlalchemy.orm import Session

from app.models import Rating
from app.schemas import RatingCreate, RatingPatch
from app.general.utils.CRUDBase import CRUDBase


class CRUDRating(CRUDBase[Rating, RatingCreate, RatingPatch]):
    def get_multi_by_artefact(
        self, db: Session, *, artefact_id: uuid.UUID,
    ) -> List[Rating]:
        return (
            db.query(self.model)
            .filter(Rating.artefact_id == artefact_id)
            .all()
        )

    def create(self, db: Session, user_id: str, rating: RatingCreate) -> Rating:
        db_obj = Rating(
            artefact_id=rating.artefact_id,
            user_id=user_id,
            value=rating.value,
            title=rating.title,
            text=rating.text,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


exportCrud = CRUDRating(Rating)

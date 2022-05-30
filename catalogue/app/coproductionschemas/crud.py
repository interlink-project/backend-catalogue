from typing import List, Optional

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.config import settings
from app.general.utils.CRUDBase import CRUDBase
from app.models import (
    CoproductionSchema,
)
from app.schemas import (
    CoproductionSchemaCreate,
    CoproductionSchemaPatch,
)


class CRUDCoproductionSchema(CRUDBase[CoproductionSchema, CoproductionSchemaCreate, CoproductionSchemaPatch]):
    async def get_multi(
        self, db: Session, search: str = "", rating: int = 0, creator: list = [], language: str = settings.DEFAULT_LANGUAGE
    ) -> List[CoproductionSchema]:
        queries = []
        if rating:
            queries.append(CoproductionSchema.rating >= rating)
        if language:
            queries.append(CoproductionSchema.languages.any(language))

        if search:
            search = search.lower()
            queries.append(or_(
                # Interlinker.tags.any(search),
                func.lower(CoproductionSchema.name_translations[language]).contains(
                    search),
                func.lower(
                    CoproductionSchema.description_translations[language]).contains(search)
            ))

        return paginate(db.query(CoproductionSchema).filter(*queries))

    async def get_public(self, db: Session, skip: int = 0, limit: int = 100) -> List[CoproductionSchema]:
        return db.query(CoproductionSchema).filter(CoproductionSchema.is_public == True).offset(skip).limit(limit).all()

    async def get_by_name(self, db: Session, name: str, locale: str) -> Optional[CoproductionSchema]:
        return db.query(CoproductionSchema).filter(CoproductionSchema.name_translations[locale] == name).first()

    # CRUD Permissions
    def can_create(self, user):
        return True

    def can_list(self, user):
        return True

    def can_read(self, user, object):
        return True

    def can_update(self, user, object):
        return True

    def can_remove(self, user, object):
        return True


exportCrud = CRUDCoproductionSchema(CoproductionSchema)


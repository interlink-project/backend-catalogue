import uuid
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.models import InterlinkerVersion, InterlinkerVersion
from app.schemas import InterlinkerVersionCreate, InterlinkerVersionPatch, InterlinkerVersionCreate
from app.general.utils.CRUDBase import CRUDBase


class CRUDInterlinkerVersion(CRUDBase[InterlinkerVersion, InterlinkerVersionCreate, InterlinkerVersionPatch]):
    def create(self, db: Session, interlinkerversion: InterlinkerVersionCreate, interlinker_id: uuid.UUID) -> InterlinkerVersion:
        db_obj = InterlinkerVersion(
            description=interlinkerversion.description,
            documentation=interlinkerversion.documentation,
            backend=interlinkerversion.backend,
            init_asset_id=interlinkerversion.init_asset_id,
            interlinker_id=interlinker_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

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


exportCrud = CRUDInterlinkerVersion(InterlinkerVersion)

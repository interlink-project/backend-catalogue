

import uuid
from typing import List

from sqlalchemy.orm import Session

from app.models import Integration
from app.schemas import IntegrationCreate, IntegrationPatch
from app.general.utils.CRUDBase import CRUDBase


class CRUDIntegration(CRUDBase[Integration, IntegrationCreate, IntegrationPatch]):
    def get_multi_by_artefact(
        self, db: Session, *, artefact_id:  uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Integration]:
        return (
            db.query(self.model)
            .filter(Integration.artefact_id == artefact_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


exportCrud = CRUDIntegration(Integration)

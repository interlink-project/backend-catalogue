

import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Integration
from app.schemas import IntegrationCreate, IntegrationPatch
from app.general.utils.CRUDBase import CRUDBase
from fastapi.encoders import jsonable_encoder


class CRUDIntegration(CRUDBase[Integration, IntegrationCreate, IntegrationPatch]):
    async def get_internal_integration_by_service_name(self, db: Session, service_name: str) -> Optional[Integration]:
        return db.query(Integration).filter(Integration.service_name == service_name).first()

exportCrud = CRUDIntegration(Integration)

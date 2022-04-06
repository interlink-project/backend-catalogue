

import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Integration, InternalIntegration, ExternalIntegration, SoftwareInterlinker
from app.schemas import IntegrationCreate, IntegrationPatch, InternalIntegrationCreate, ExternalIntegrationCreate
from app.general.utils.CRUDBase import CRUDBase
from fastapi.encoders import jsonable_encoder


class CRUDIntegration(CRUDBase[Integration, IntegrationCreate, IntegrationPatch]):
    async def create(self, db: Session, obj_in: IntegrationCreate) -> Integration:
        json_compatible_item_data = jsonable_encoder(obj_in)
        if type(obj_in) == InternalIntegrationCreate:
            db_obj = InternalIntegration(**json_compatible_item_data)

        if type(obj_in) == ExternalIntegrationCreate:
            db_obj = ExternalIntegration(**json_compatible_item_data)

        db.add(db_obj)
        db.commit()
        return db_obj

    async def get_internal_integration_by_service_name(self, db: Session, service_name: str) -> Optional[InternalIntegration]:
        return db.query(InternalIntegration).filter(InternalIntegration.service_name == service_name).first()

exportCrud = CRUDIntegration(Integration)



import uuid
from typing import List

from sqlalchemy.orm import Session

from app.models import Integration
from app.schemas import IntegrationCreate, IntegrationPatch
from app.general.utils.CRUDBase import CRUDBase


class CRUDIntegration(CRUDBase[Integration, IntegrationCreate, IntegrationPatch]):
    pass

exportCrud = CRUDIntegration(Integration)

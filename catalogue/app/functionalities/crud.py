
import uuid
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.models import Functionality
from app.schemas import FunctionalityCreate, FunctionalityPatch
from app.general.utils.CRUDBase import CRUDBase


class CRUDFunctionality(CRUDBase[Functionality, FunctionalityCreate, FunctionalityPatch]):
    def get_by_name(self, db: Session, name: str) -> Optional[Functionality]:
        return db.query(Functionality).filter(Functionality.name == name).first()

    def create(self, db: Session, *, functionality: FunctionalityCreate) -> Functionality:
        db_obj = Functionality(
            name=functionality.name,
            description=functionality.description,
            functionalities=functionality.functionalities,
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

exportCrud = CRUDFunctionality(Functionality)

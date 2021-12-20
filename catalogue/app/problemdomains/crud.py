
import uuid
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.models import ProblemDomain
from app.schemas import ProblemDomainCreate, ProblemDomainPatch
from app.general.utils.CRUDBase import CRUDBase


class CRUDProblemDomain(CRUDBase[ProblemDomain, ProblemDomainCreate, ProblemDomainPatch]):
    def get_by_name(self, db: Session, name: str) -> Optional[ProblemDomain]:
        return db.query(ProblemDomain).filter(ProblemDomain.name == name).first()

    def create(self, db: Session, *, problemdomain: ProblemDomainCreate) -> ProblemDomain:
        db_obj = ProblemDomain(
            name=problemdomain.name,
            description=problemdomain.description,
            functionalities=problemdomain.functionalities,
            target_stakeholder_groups=problemdomain.target_stakeholder_groups,
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

exportCrud = CRUDProblemDomain(ProblemDomain)

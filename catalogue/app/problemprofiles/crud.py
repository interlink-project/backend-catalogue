
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.models import ProblemProfile
from app.schemas import ProblemProfileCreate, ProblemProfilePatch
from app.general.utils.CRUDBase import CRUDBase


class CRUDProblemProfile(CRUDBase[ProblemProfile, ProblemProfileCreate, ProblemProfilePatch]):
    async def get_by_name(self, db: Session, name: str, locale: str) -> Optional[ProblemProfile]:
        return db.query(ProblemProfile).filter(ProblemProfile.name_translations[locale] == name).first()

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

exportCrud = CRUDProblemProfile(ProblemProfile, logByDefault=True)

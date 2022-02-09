
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.models import ProblemProfile
from app.schemas import ProblemProfileCreate, ProblemProfilePatch
from app.general.utils.CRUDBase import CRUDBase


class CRUDProblemProfile(CRUDBase[ProblemProfile, ProblemProfileCreate, ProblemProfilePatch]):
    def get_by_name(self, db: Session, name: str, locale: str) -> Optional[ProblemProfile]:
        return db.query(ProblemProfile).filter(ProblemProfile.name_translations[locale] == name).first()

    def create(self, db: Session, *, problemprofile: ProblemProfileCreate) -> ProblemProfile:
        db_obj = ProblemProfile(
            id=problemprofile.id,
            name_translations=problemprofile.name_translations,
            description_translations=problemprofile.description_translations,
            functionality_translations=problemprofile.functionality_translations,
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

exportCrud = CRUDProblemProfile(ProblemProfile)

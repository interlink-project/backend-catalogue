

import uuid
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.models import PublicService
from app.schemas import PublicServiceCreate, PublicServicePatch
from app.general.utils.CRUDBase import CRUDBase


class CRUDPublicService(CRUDBase[PublicService, PublicServiceCreate, PublicServicePatch]):
    def get_by_name(self, db: Session, name: str, language:str = "en") -> Optional[PublicService]:
        return db.query(PublicService).filter(PublicService.name_translations[language] == name).first()

    def create(self, db: Session, *, publicservice: PublicServiceCreate) -> PublicService:
        db_obj = PublicService(
            artefact_type="publicservice",
            name_translations=publicservice.name_translations,
            description_translations=publicservice.description_translations,
            logotype=publicservice.logotype,
            snapshots=publicservice.snapshots,
            published=publicservice.published,
            tags=publicservice.tags,
            # Public Service specific
            language=publicservice.language,
            processing_time=publicservice.processing_time,
            location=publicservice.location,
            status=publicservice.status,
            public_organization=publicservice.public_organization,
            output=publicservice.output,
            cost=publicservice.cost,
        )
        """
        for pr_id in interlinker.publicservices:
        publicservice = get_publicservice(session, pr_id)
        session_interlinker.publicservices.append(publicservice)
        """
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

exportCrud = CRUDPublicService(PublicService)

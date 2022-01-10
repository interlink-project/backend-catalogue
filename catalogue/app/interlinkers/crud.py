from typing import Optional

from sqlalchemy.orm import Session

from app.models import Interlinker
from app.schemas import InterlinkerCreate, InterlinkerPatch
from app.general.utils.CRUDBase import CRUDBase

class CRUDInterlinker(CRUDBase[Interlinker, InterlinkerCreate, InterlinkerPatch]):
    def get_by_name(self, db: Session, name: str) -> Optional[Interlinker]:
        return db.query(Interlinker).filter(Interlinker.name == name).first()

    def create(self, db: Session, *, interlinker: InterlinkerCreate) -> Interlinker:
        db_obj = Interlinker(
            # Artefact
            name=interlinker.name,
            description=interlinker.description,
            logotype=interlinker.logotype,
            images=interlinker.images,
            published=interlinker.published,
            keywords=interlinker.keywords,
            documentation=interlinker.documentation,
            # Interlinker specific
            SOC_type=interlinker.SOC_type,
            nature=interlinker.nature,
            administrative_scope=interlinker.administrative_scope,
            specific_app_domain=interlinker.specific_app_domain,
            constraints=interlinker.constraints,
            regulations=interlinker.regulations,
            software_type=interlinker.software_type,
            software_implementation=interlinker.software_implementation,
            software_customization=interlinker.software_customization,
            software_integration=interlinker.software_integration,
            knowledge_type=interlinker.knowledge_type,
            knowledge_format=interlinker.knowledge_format,
            # Version
            backend=interlinker.backend,
            init_asset_id=interlinker.init_asset_id,
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

exportCrud = CRUDInterlinker(Interlinker)

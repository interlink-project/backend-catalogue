from sys import implementation
from typing import Optional, List, Union

from sqlalchemy.orm import Session

from app.models import Interlinker, KnowledgeInterlinker, SoftwareInterlinker
from app.schemas import InterlinkerCreate, SoftwareInterlinkerCreate, KnowledgeInterlinkerCreate, InterlinkerPatch
from app.general.utils.CRUDBase import CRUDBase
from sqlalchemy import or_, func
from app.exceptions import CrudException

class CRUDInterlinker(CRUDBase[Interlinker, InterlinkerCreate, InterlinkerPatch]):
    def get_by_name(self, db: Session, name: str) -> Optional[Interlinker]:
        return db.query(Interlinker).filter(Interlinker.name == name).first()

    def get_multi_knowledgeinterlinkers(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[KnowledgeInterlinker]:
        return db.query(KnowledgeInterlinker).offset(skip).limit(limit).all()

    def get_multi_softwareinterlinkers(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[SoftwareInterlinker]:
        return db.query(SoftwareInterlinker).offset(skip).limit(limit).all()

    def get_softwareinterlinker_by_backend(self, db: Session, backend: str) -> Optional[SoftwareInterlinker]:
        return db.query(SoftwareInterlinker).filter(SoftwareInterlinker.backend == backend).first()

    def create(self, db: Session, *, interlinker: InterlinkerCreate) -> Interlinker:
        data = {
                # Artefact
                "artefact_type": "interlinker",
                "name": interlinker.name,
                "description": interlinker.description,
                "logotype": interlinker.logotype,
                "images": interlinker.images,
                "published": interlinker.published,
                "keywords": interlinker.keywords,
                "documentation": interlinker.documentation,
                # Interlinker
                "nature": interlinker.nature,
                "constraints": interlinker.constraints,
                "regulations": interlinker.regulations,
            }
        if type(interlinker) == SoftwareInterlinkerCreate:
            print("IS SOFTWARE")
            # Software interlinker specific
            data["backend"] = interlinker.backend
            data["assets_deletable"] = interlinker.assets_deletable
            data["assets_updatable"] = interlinker.assets_updatable
            data["assets_clonable"] = interlinker.assets_clonable
            db_obj = SoftwareInterlinker(**data)
        if type(interlinker) == KnowledgeInterlinkerCreate:
            print("IS KNOWLEDGE")
            # Knowledge interlinker specific
            software_interlinker = self.get(db, interlinker.softwareinterlinker_id)
            if not software_interlinker:
                raise CrudException("Software interlinker does not exist")
            print(software_interlinker.__dict__)
            data["softwareinterlinker_id"] = interlinker.softwareinterlinker_id
            data["genesis_asset_id"] = interlinker.genesis_asset_id
            db_obj = KnowledgeInterlinker(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, search: str = ""
    ) -> List[Interlinker]:
        if search != "":
            search = search.lower()
            print(f"SEARCHING FOR {search}")
            return db.query(Interlinker).filter(
                or_(
                    func.lower(Interlinker.keywords).contains(search), 
                    func.lower(Interlinker.name).contains(search)
                )
            ).offset(skip).limit(limit).all()
        return db.query(Interlinker).offset(skip).limit(limit).all()

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

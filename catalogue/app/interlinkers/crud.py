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

    def get_softwareinterlinker_by_path(self, db: Session, path: str) -> Optional[SoftwareInterlinker]:
        return db.query(SoftwareInterlinker).filter(SoftwareInterlinker.path == path).first()

    def create(self, db: Session, *, interlinker: InterlinkerCreate) -> Interlinker:
        data = {
                # Artefact
                "artefact_type": "interlinker",
                "name": interlinker.name,
                "description": interlinker.description,
                "logotype": interlinker.logotype,
                "snapshots": interlinker.snapshots,
                "published": interlinker.published,
                "tags": interlinker.tags,
                # Interlinker
                "nature": interlinker.nature,
                "difficulty": interlinker.difficulty,
                "targets": interlinker.targets,
                "licence": interlinker.licence,
                "problem_profiles": interlinker.problem_profiles,
                "types": interlinker.types,
                # "related_interlinkers":interlinker.related_interlinkers,
                "administrative_scopes": interlinker.administrative_scopes,
                "domain": interlinker.domain,
                "process": interlinker.process,
                "constraints_and_limitations": interlinker.constraints_and_limitations,
                "regulations_and_standards": interlinker.regulations_and_standards,
            }
        if type(interlinker) == SoftwareInterlinkerCreate:
            print("IS SOFTWARE")
            # Software interlinker specific
            data["supported_by"] = interlinker.supported_by
            data["auth_method"] = interlinker.auth_method
            data["deployment_manual"] = interlinker.deployment_manual
            data["user_manual"] = interlinker.user_manual
            data["developer_manual"] = interlinker.developer_manual
            data["supports_internationalization"] = interlinker.supports_internationalization
            data["is_responsive"] = interlinker.is_responsive
            data["open_in_modal"] = interlinker.open_in_modal
            data["assets_clonable"] = interlinker.assets_clonable
            data["path"] = interlinker.path
            data["is_subdomain"] = interlinker.is_subdomain

            db_obj = SoftwareInterlinker(**data)
        if type(interlinker) == KnowledgeInterlinkerCreate:
            print("IS KNOWLEDGE")
            # Knowledge interlinker specific
            software_interlinker = self.get(db, interlinker.softwareinterlinker_id)
            if not software_interlinker:
                raise CrudException("Software interlinker does not exist")
            data["softwareinterlinker_id"] = interlinker.softwareinterlinker_id
            data["genesis_asset_id"] = interlinker.genesis_asset_id
            data["form"] = interlinker.form
            data["format"] = interlinker.format
            data["instructions"] = interlinker.instructions
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

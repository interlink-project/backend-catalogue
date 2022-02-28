from sys import implementation
from typing import Optional, List, Union

from sqlalchemy.orm import Session

from app.models import Interlinker, KnowledgeInterlinker, SoftwareInterlinker
from app.schemas import InterlinkerCreate, SoftwareInterlinkerCreate, KnowledgeInterlinkerCreate, InterlinkerPatch
from app.general.utils.CRUDBase import CRUDBase
from sqlalchemy import or_, func
from app.exceptions import CrudException
from app.problemprofiles.crud import exportCrud as problems_crud
from app.problemprofiles.models import ProblemProfile
from app.integrations.models import Integration
from sqlalchemy import and_

class CRUDInterlinker(CRUDBase[Interlinker, InterlinkerCreate, InterlinkerPatch]):
    def get_by_name(self, db: Session, name: str, language: str ="en") -> Optional[Interlinker]:
        return db.query(Interlinker).filter(Interlinker.name_translations[language] == name).first()

    def get_multi_knowledgeinterlinkers(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[KnowledgeInterlinker]:
        return db.query(KnowledgeInterlinker).offset(skip).limit(limit).all()

    def get_multi_softwareinterlinkers(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[SoftwareInterlinker]:
        return db.query(SoftwareInterlinker).offset(skip).limit(limit).all()
    
    def get_multi_integrated_softwareinterlinkers(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[SoftwareInterlinker]:
        return db.query(SoftwareInterlinker).filter(and_(Integration.service_name != None, Integration.shortcut == True)).offset(skip).limit(limit).all()

    def get_softwareinterlinker_by_service_name(self, db: Session, service_name: str) -> Optional[SoftwareInterlinker]:
        return db.query(SoftwareInterlinker).filter(SoftwareInterlinker.id == Integration.softwareinterlinker_id).filter(Integration.service_name == service_name).first()

    def create(self, db: Session, *, interlinker: InterlinkerCreate) -> Interlinker:
        data = {
                # Artefact
                "artefact_type": "interlinker",
                "name_translations": interlinker.name_translations,
                "description_translations": interlinker.description_translations,
                "logotype": interlinker.logotype,
                "snapshots": interlinker.snapshots,
                "published": interlinker.published,
                "tags": interlinker.tags,
                # Interlinker
                "nature": interlinker.nature,
                "difficulty": interlinker.difficulty,
                "targets": interlinker.targets,
                "licence": interlinker.licence,
                "types": interlinker.types,
                # "related_interlinkers":interlinker.related_interlinkers,
                "administrative_scopes": interlinker.administrative_scopes,
                "process": interlinker.process,
                "constraints_and_limitations_translations": interlinker.constraints_and_limitations_translations,
                "regulations_and_standards_translations": interlinker.regulations_and_standards_translations,
            }
        if type(interlinker) == SoftwareInterlinkerCreate:
            print("IS SOFTWARE")
            # Software interlinker specific
            data["supported_by"] = interlinker.supported_by
            data["deployment_manual"] = interlinker.deployment_manual
            data["user_manual"] = interlinker.user_manual
            data["developer_manual"] = interlinker.developer_manual
            data["supports_internationalization"] = interlinker.supports_internationalization
            data["is_responsive"] = interlinker.is_responsive

            db_obj = SoftwareInterlinker(**data)
        if type(interlinker) == KnowledgeInterlinkerCreate:
            print("IS KNOWLEDGE")
            db_obj = KnowledgeInterlinker(**data)
        db.add(db_obj)
        db.commit()

        for id in interlinker.problem_profiles:
            print(id)
            problem = problems_crud.get(db=db, id=id)
            db_obj.problemprofiles.append(problem)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, search: str = "", language: str = "en"
    ) -> List[Interlinker]:
        if search != "":
            search = search.lower()
            return db.query(Interlinker).filter(
                or_(
                    Interlinker.tags.any(search), 
                    func.lower(Interlinker.name_translations[language]).contains(search),
                    func.lower(Interlinker.description_translations[language]).contains(search)
                )
            ).offset(skip).limit(limit).all()
        return db.query(Interlinker).offset(skip).limit(limit).all()
    
    def get_by_problem_profiles(
        self, db: Session, *, skip: int = 0, limit: int = 100, problem_profiles: list
    ) -> List[Interlinker]:
        
        return db.query(Interlinker).filter(Interlinker.problemprofiles.any(ProblemProfile.id.in_(problem_profiles))).offset(skip).limit(limit).all()

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

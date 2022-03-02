from sys import implementation
from typing import Optional, List, Union

from sqlalchemy.orm import Session

from app.models import Interlinker, KnowledgeInterlinker, SoftwareInterlinker
from app.schemas import InterlinkerCreate, SoftwareInterlinkerCreate, KnowledgeInterlinkerCreate, InterlinkerPatch
from app.general.utils.CRUDBase import CRUDBase
from sqlalchemy import or_, func
from app.exceptions import CrudException
from app.problemprofiles.crud import exportCrud as problems_crud
from app.models import ProblemProfile
from app.integrations.models import Integration
from sqlalchemy import and_, or_
import uuid
from fastapi_pagination.ext.sqlalchemy import paginate


class CRUDInterlinker(CRUDBase[Interlinker, InterlinkerCreate, InterlinkerPatch]):
    def get_by_name(self, db: Session, name: str, language: str = "en") -> Optional[Interlinker]:
        return db.query(Interlinker).filter(
            Interlinker.name_translations[language] == name
        ).first()

    def get_knowledgeinterlinker(self, db: Session, id: uuid.UUID) -> Optional[KnowledgeInterlinker]:
        return db.query(KnowledgeInterlinker).filter(
            KnowledgeInterlinker.id == id,
        ).first()

    def get_multi_knowledgeinterlinkers(
        self, db: Session
    ) -> List[KnowledgeInterlinker]:
        return paginate(db.query(KnowledgeInterlinker))

    def get_multi_softwareinterlinkers(
        self, db: Session
    ) -> List[SoftwareInterlinker]:
        return paginate(db.query(SoftwareInterlinker))

    def get_multi_integrated_softwareinterlinkers(
        self, db: Session
    ) -> List[SoftwareInterlinker]:
        return db.query(SoftwareInterlinker).filter(and_(Integration.service_name != None, Integration.shortcut == True)).all()

    def get_softwareinterlinker_by_service_name(self, db: Session, service_name: str) -> Optional[SoftwareInterlinker]:
        return db.query(SoftwareInterlinker).filter(SoftwareInterlinker.id == Integration.softwareinterlinker_id).filter(Integration.service_name == service_name).first()

    def create(self, db: Session, *, interlinker: InterlinkerCreate) -> Interlinker:
        data = {}
        data["artefact_type"] = "interlinker"
        data["name_translations"] = interlinker.name_translations
        data["description_translations"] = interlinker.description_translations
        data["constraints_and_limitations_translations"] = interlinker.constraints_and_limitations_translations
        data["regulations_and_standards_translations"] = interlinker.regulations_and_standards_translations
        data["tags_translations"] = interlinker.tags_translations
        data["creator_id"] = interlinker.creator_id

        # Interlinker
        data["logotype"] = interlinker.logotype
        data["snapshots"] = interlinker.snapshots
        data["published"] = interlinker.published
        data["nature"] = interlinker.nature
        data["difficulty"] = interlinker.difficulty
        data["targets"] = interlinker.targets
        data["licence"] = interlinker.licence
        data["types"] = interlinker.types

        data["administrative_scopes"] = interlinker.administrative_scopes
        data["process"] = interlinker.process

        if type(interlinker) == SoftwareInterlinkerCreate:
            print("IS SOFTWARE")
            # Software interlinker specific
            data["nature"] = "softwareinterlinker"
            data["supported_by"] = interlinker.supported_by
            data["deployment_manual"] = interlinker.deployment_manual
            data["user_manual"] = interlinker.user_manual
            data["developer_manual"] = interlinker.developer_manual
            data["supports_internationalization"] = interlinker.supports_internationalization
            data["is_responsive"] = interlinker.is_responsive
            db_obj = SoftwareInterlinker(**data)

        if type(interlinker) == KnowledgeInterlinkerCreate:
            data["nature"] = "knowledgeinterlinker"
            data["languages"] = interlinker.languages
            data["form"] = interlinker.form
            data["format"] = interlinker.format
            data["instructions_translations"] = interlinker.instructions_translations
            data["softwareinterlinker_id"] = interlinker.softwareinterlinker_id
            data["genesis_asset_id_translations"] = interlinker.genesis_asset_id_translations

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
        self, db: Session, search: str = "", natures: list = [], creator: list = [], language: str = "en"
    ) -> List[Interlinker]:
        queries = []
        if search:
            search = search.lower()
            queries.append(or_(
                    # Interlinker.tags.any(search),
                    func.lower(Interlinker.name_translations[language]).contains(
                        search),
                    func.lower(
                        Interlinker.description_translations[language]).contains(search)
                ))
        
        if natures:
            queries.append(
                Interlinker.nature.in_(natures)
            )
        
        # if creator:
        #     queries.append(
        #         Interlinker.creator_id != None
        #     )
        return paginate(db.query(Interlinker).filter(*queries))
    
    def get_related(
        self, db: Session, interlinker: Interlinker
    ) -> List[Interlinker]:
        return paginate(db.query(Interlinker).filter(
            or_(
                Interlinker.problemprofiles.any(ProblemProfile.id.in_(interlinker.problemprofiles)),
            )
        ))

    def get_by_problem_profiles(
        self, db: Session, problem_profiles: list, exclude: list = []
    ) -> List[Interlinker]:

        return paginate(db.query(Interlinker).filter(
            and_(
                Interlinker.problemprofiles.any(ProblemProfile.id.in_(problem_profiles)),
                Interlinker.id.not_in(exclude)
            )
        ))
       

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
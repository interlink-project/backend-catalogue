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
from app.integrations.models import Integration, InternalIntegration
from sqlalchemy import and_, or_
import uuid
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi.encoders import jsonable_encoder

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

    def get_multi_internally_integrated_softwareinterlinkers(
        self, db: Session
    ) -> List[SoftwareInterlinker]:
        return db.query(SoftwareInterlinker).filter(Integration.softwareinterlinker_id == SoftwareInterlinker.id).filter(InternalIntegration.id == Integration.id).filter(and_(InternalIntegration.service_name != None, InternalIntegration.shortcut == True)).all()

    def get_softwareinterlinker_by_service_name(self, db: Session, service_name: str) -> Optional[SoftwareInterlinker]:
        return db.query(SoftwareInterlinker).filter(SoftwareInterlinker.id == Integration.softwareinterlinker_id).filter(InternalIntegration.id == Integration.id).filter(InternalIntegration.service_name == service_name).first()

    def create(self, db: Session, *, interlinker: InterlinkerCreate) -> Interlinker:
        data = jsonable_encoder(interlinker)

        data["artefact_type"] = "interlinker"
        del data["problem_profiles"]

        if type(interlinker) == SoftwareInterlinkerCreate:
            print("IS SOFTWARE")
            data["nature"] = "softwareinterlinker"
            db_obj = SoftwareInterlinker(**data)

        if type(interlinker) == KnowledgeInterlinkerCreate:
            print("IS KNOWLEDGE")
            data["nature"] = "knowledgeinterlinker"
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
        self, db: Session, search: str = "", natures: list = [], rating: int = 0, creator: list = [], language: str = "en"
    ) -> List[Interlinker]:
        queries = []

        if rating:
            queries.append(Interlinker.rating >= rating)
            
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
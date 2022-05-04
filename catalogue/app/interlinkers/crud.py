from sys import implementation
from typing import Optional, List, Union

from sqlalchemy.orm import Session

from app.models import Interlinker, KnowledgeInterlinker, SoftwareInterlinker, ExternalSoftwareInterlinker, ExternalKnowledgeInterlinker
from app.schemas import InterlinkerCreate, SoftwareInterlinkerCreate, KnowledgeInterlinkerCreate, ExternalKnowledgeInterlinkerCreate, ExternalSoftwareInterlinkerCreate, InterlinkerPatch
from app.general.utils.CRUDBase import CRUDBase
from sqlalchemy import or_, func
from app.problemprofiles.crud import exportCrud as problems_crud
from app.models import ProblemProfile
from app.integrations.models import Integration
from sqlalchemy import and_, or_
import uuid
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi.encoders import jsonable_encoder
from app.messages import log
from app.config import settings

class CRUDInterlinker(CRUDBase[Interlinker, InterlinkerCreate, InterlinkerPatch]):
    async def get_by_name(self, db: Session, name: str, language: str = settings.DEFAULT_LANGUAGE) -> Optional[Interlinker]:
        return db.query(Interlinker).filter(
            Interlinker.name_translations[language] == name
        ).first()

    async def get_knowledgeinterlinker(self, db: Session, id: uuid.UUID) -> Optional[KnowledgeInterlinker]:
        ki = db.query(KnowledgeInterlinker).filter(
            KnowledgeInterlinker.id == id,
        ).first()
        if ki:
            await log({
                "model": "KNOWLEDGEINTERLINKER",
                "action": "GET",
                "id": id
            })
        return ki

    async def get_multi_knowledgeinterlinkers(
        self, db: Session
    ) -> List[KnowledgeInterlinker]:
        await log({
                "model": "KNOWLEDGEINTERLINKER",
                "action": "LIST",
            })
        return paginate(db.query(KnowledgeInterlinker))

    async def get_multi_softwareinterlinkers(
        self, db: Session
    ) -> List[SoftwareInterlinker]:
        await log({
            "model": "SOFTWAREINTERLINKER",
            "action": "LIST",
        })
        return paginate(db.query(SoftwareInterlinker))

    async def get_multi_externalsoftwareinterlinkers(
        self, db: Session
    ) -> List[ExternalSoftwareInterlinker]:
        await log({
            "model": "EXTERNALSOFTWAREINTERLINKER",
            "action": "LIST",
        })
        return paginate(db.query(ExternalSoftwareInterlinker))

    async def get_multi_externalknowledgeinterlinkers(
        self, db: Session
    ) -> List[ExternalKnowledgeInterlinker]:
        await log({
            "model": "EXTERNALKNOWLEDGEINTERLINKER",
            "action": "LIST",
        })
        return paginate(db.query(ExternalKnowledgeInterlinker))

    async def get_multi_internally_integrated_softwareinterlinkers(
        self, db: Session
    ) -> List[SoftwareInterlinker]:
        await log({
            "model": "SOFTWAREINTERLINKER",
            "action": "LIST_SHORTCUT",
        })
        return db.query(SoftwareInterlinker).filter(Integration.softwareinterlinker_id == SoftwareInterlinker.id).filter(and_(Integration.service_name != None, Integration.shortcut == True)).all()

    async def get_softwareinterlinker_by_service_name(self, db: Session, service_name: str) -> Optional[SoftwareInterlinker]:
        await log({
            "model": "SOFTWAREINTERLINKER",
            "action": "GET_BY_SERVICE_NAME",
        })
        return db.query(SoftwareInterlinker).filter(SoftwareInterlinker.id == Integration.softwareinterlinker_id).filter(Integration.service_name == service_name).first()

    async def create(self, db: Session, *, interlinker: InterlinkerCreate) -> Interlinker:
        data = jsonable_encoder(interlinker)
        data["artefact_type"] = "interlinker"
        problemprofiles = data["problemprofiles"]
        # delete before creating interlinker because it is a list of strings, not a list of problem profile objects
        del data["problemprofiles"]

        db_obj = None
        if type(interlinker) == SoftwareInterlinkerCreate:
            print("IS SOFTWARE")
            data["nature"] = "softwareinterlinker"
            db_obj = SoftwareInterlinker(**data)

        elif type(interlinker) == KnowledgeInterlinkerCreate:
            print("IS KNOWLEDGE")
            data["nature"] = "knowledgeinterlinker"
            db_obj = KnowledgeInterlinker(**data)
        
        elif type(interlinker) == ExternalSoftwareInterlinkerCreate or type(interlinker) == ExternalKnowledgeInterlinkerCreate:
            if data["nature"] == "externalsoftwareinterlinker":
                print("IS EXTERNAL SOFTWARE")
                db_obj = ExternalSoftwareInterlinker(**data)
            else:
                print("IS EXTERNAL KNOWLEDGE")
                db_obj = ExternalKnowledgeInterlinker(**data)
            
        
        for id in problemprofiles:
            print(id)
            if problem := await problems_crud.get(db=db, id=id):
                db_obj.problemprofiles.append(problem)
        
        db.add(db_obj)
        db.commit()
        await log({
            "model": db_obj.__class__.__name__.upper(),
            "action": "CREATE",
        })
        db.refresh(db_obj)
        return db_obj

    async def get_multi(
        self, db: Session, search: str = "", natures: list = [], rating: int = 0, creator: list = [], language: str = "en"
    ) -> List[Interlinker]:
        queries = []

        if rating:
            queries.append(Interlinker.rating >= rating)
        
        if language:
            queries.append(Interlinker.languages.any(language))

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
        await log({
            "model": self.modelName,
            "action": "GET_MULTI",
            "search": search,
            "rating": rating,
            "natures": natures
        })
        return paginate(db.query(Interlinker).filter(*queries))
    
    async def get_related(
        self, db: Session, interlinker: Interlinker
    ) -> List[Interlinker]:
        await log({
            "model": self.modelName,
            "action": "GET_RELATED",
            "interlinker_id": interlinker.id
        })
        return paginate(db.query(Interlinker).filter(
            or_(
                Interlinker.problemprofiles.any(ProblemProfile.id.in_(interlinker.problemprofiles)),
            )
        ))

    async def get_by_problemprofiles(
        self, db: Session, problemprofiles: list, exclude: list = [], language: str = settings.DEFAULT_LANGUAGE
    ) -> List[Interlinker]:
        await log({
            "model": self.modelName,
            "action": "GET_BY_PROBLEMPROFILES",
            "problemprofiles": problemprofiles,
        })
        queries = [
            and_(
                Interlinker.problemprofiles.any(ProblemProfile.id.in_(problemprofiles)),
                Interlinker.id.not_in(exclude)
            )
        ]
        
        if language:
            queries.append(Interlinker.languages.any(language))

        return paginate(db.query(Interlinker).filter(*queries))
       
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
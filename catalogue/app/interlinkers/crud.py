import uuid
from typing import Any, Dict, List, Optional, Union

from fastapi.encoders import jsonable_encoder
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from app.config import settings
from app.general.utils.CRUDBase import CRUDBase
from app.messages import log
from app.models import (
    ExternalKnowledgeInterlinker,
    ExternalSoftwareInterlinker,
    Interlinker,
    KnowledgeInterlinker,
    ProblemProfile,
    SoftwareInterlinker,
)
from app.problemprofiles.crud import exportCrud as problems_crud
from app.schemas import (
    ExternalKnowledgeInterlinkerCreate,
    ExternalSoftwareInterlinkerCreate,
    KnowledgeInterlinkerCreate,
    SoftwareInterlinkerCreate,
    ExternalKnowledgeInterlinkerPatch,
    ExternalSoftwareInterlinkerPatch,
    KnowledgeInterlinkerPatch,
    SoftwareInterlinkerPatch,
    InterlinkerCreate,
    InterlinkerPatch,
)


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

    async def get_softwareinterlinker_by_service_name(self, db: Session, service_name: str) -> Optional[SoftwareInterlinker]:
        await log({
            "model": "SOFTWAREINTERLINKER",
            "action": "GET_BY_SERVICE_NAME",
        })
        return db.query(SoftwareInterlinker).filter(SoftwareInterlinker.service_name == service_name).first()

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
        
        elif type(interlinker) in [ExternalSoftwareInterlinkerCreate, ExternalKnowledgeInterlinkerCreate]:
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
        self, db: Session, exclude: list = [], search: str = "", problemprofiles: list = [], natures: list = [], rating: int = 0, creator: list = [], language: str = "en"
    ) -> List[Interlinker]:
        queries = []

        if rating:
            queries.append(Interlinker.rating >= rating)
        
        if language:
            queries.append(Interlinker.languages.any(language))
        
        if problemprofiles:
            queries.append(Interlinker.problemprofiles.any(ProblemProfile.id.in_(problemprofiles)))
            
        if search:
            search = search.lower()
            queries.append(or_(
                    func.lower(Interlinker.tags_translations[language]).contains(
                        search),
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
        return paginate(db.query(Interlinker).filter(*queries, Interlinker.id.not_in(exclude)))
    
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

    async def update(
        self,
        db: Session,
        *,
        db_obj: Union[ExternalKnowledgeInterlinker, ExternalSoftwareInterlinker, SoftwareInterlinker, KnowledgeInterlinker],
        obj_in: Union[ExternalKnowledgeInterlinkerPatch, ExternalSoftwareInterlinkerPatch, SoftwareInterlinkerPatch, KnowledgeInterlinkerPatch, Dict[str, Any]]
    ) -> Interlinker:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for id in update_data.get("problemprofiles", []):
            if problem := await problems_crud.get(db=db, id=id):
                db_obj.problemprofiles.append(problem)
        del update_data["problemprofiles"]
        
        for field, value in update_data.items():
            if hasattr(db_obj, field) and value != getattr(db_obj, field):
                print("Updating", field)
                setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        await log({
            "model": self.modelName,
            "action": "UPDATE",
            "id": db_obj.id
        })
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

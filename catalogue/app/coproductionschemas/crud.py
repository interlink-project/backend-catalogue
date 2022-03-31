from typing import Optional, List

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.general.utils.CRUDBase import CRUDBase
from app.models import (
    CoproductionSchema,
    ObjectiveMetadata,
    PhaseMetadata,
    TaskMetadata,
)
from app.problemprofiles.crud import exportCrud as problemprofilesCrud
from app.schemas import CoproductionSchemaCreate, CoproductionSchemaPatch, TaskMetadataCreate, TaskMetadataPatch, ObjectiveMetadataCreate, ObjectiveMetadataPatch, PhaseMetadataCreate, PhaseMetadataPatch


class CRUDCoproductionSchema(CRUDBase[CoproductionSchema, CoproductionSchemaCreate, CoproductionSchemaPatch]):
    def get_multi(
        self, db: Session, search: str = "", rating: int = 0, creator: list = [], language: str = "en"
    ) -> List[CoproductionSchema]:
        queries = []
        if rating:
            queries.append(CoproductionSchema.rating >= rating)

        if search:
            search = search.lower()
            queries.append(or_(
                # Interlinker.tags.any(search),
                func.lower(CoproductionSchema.name_translations[language]).contains(
                    search),
                func.lower(
                    CoproductionSchema.description_translations[language]).contains(search)
            ))

        return paginate(db.query(CoproductionSchema).filter(*queries))

    def get_public(self, db: Session, skip: int = 0, limit: int = 100) -> List[CoproductionSchema]:
        return db.query(CoproductionSchema).filter(CoproductionSchema.is_public == True).offset(skip).limit(limit).all()

    def get_by_name(self, db: Session, name: str, locale: str) -> Optional[CoproductionSchema]:
        return db.query(CoproductionSchema).filter(CoproductionSchema.name_translations[locale] == name).first()

    def create(self, db: Session, coproductionschema: CoproductionSchemaCreate) -> CoproductionSchema:
        db_obj = CoproductionSchema(
            name_translations=coproductionschema.name_translations,
            description_translations=coproductionschema.description_translations,
            is_public=coproductionschema.is_public,
            author=coproductionschema.author,
            licence=coproductionschema.licence,
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


exportCrud = CRUDCoproductionSchema(CoproductionSchema)


class CRUDObjectiveMetadata(CRUDBase[ObjectiveMetadata, ObjectiveMetadataCreate, ObjectiveMetadataPatch]):

    def get_by_name(self, db: Session, name: str, language: str = "en") -> Optional[ObjectiveMetadata]:
        return db.query(ObjectiveMetadata).filter(ObjectiveMetadata.name_translations[language] == name).first()

    def create(self, db: Session, *, objectivemetadata: ObjectiveMetadataCreate) -> ObjectiveMetadata:
        db_obj = ObjectiveMetadata(
            name_translations=objectivemetadata.name_translations,
            description_translations=objectivemetadata.description_translations,
            # relations
            phasemetadata_id=objectivemetadata.phasemetadata_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_prerequisite(self, db: Session, objectivemetadata: ObjectiveMetadata, prerequisite: ObjectiveMetadata) -> ObjectiveMetadata:
        if objectivemetadata.id == prerequisite.id:
            raise Exception("Same object")
        objectivemetadata.prerequisites.append(prerequisite)
        db.commit()
        db.refresh(objectivemetadata)
        return objectivemetadata

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


objectivesExportCrud = CRUDObjectiveMetadata(ObjectiveMetadata)


class CRUDPhaseMetadata(CRUDBase[PhaseMetadata, PhaseMetadataCreate, PhaseMetadataPatch]):
    def create(self, db: Session, phasemetadata: PhaseMetadataCreate) -> PhaseMetadata:
        db_obj = PhaseMetadata(
            name_translations=phasemetadata.name_translations,
            description_translations=phasemetadata.description_translations,
            # relations
            coproductionschema_id=phasemetadata.coproductionschema_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_name(self, db: Session, name: str, language: str = "en") -> Optional[PhaseMetadata]:
        return db.query(PhaseMetadata).filter(PhaseMetadata.name_translations[language] == name).first()

    def add_prerequisite(self, db: Session, phasemetadata: PhaseMetadata, prerequisite: PhaseMetadata) -> PhaseMetadata:
        if phasemetadata.id == prerequisite.id:
            raise Exception("Same object")
        phasemetadata.prerequisites.append(prerequisite)
        db.commit()
        db.refresh(phasemetadata)
        return phasemetadata

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


phasesExportCrud = CRUDPhaseMetadata(PhaseMetadata)


class CRUDTaskMetadata(CRUDBase[TaskMetadata, TaskMetadataCreate, TaskMetadataPatch]):

    def get_by_name(self, db: Session, name: str, language: str = "en") -> Optional[TaskMetadata]:
        return db.query(TaskMetadata).filter(TaskMetadata.name_translations[language] == name).first()

    def add_prerequisite(self, db: Session, taskmetadata: TaskMetadata, prerequisite: TaskMetadata) -> TaskMetadata:
        if taskmetadata.id == prerequisite.id:
            raise Exception("Same object")
        taskmetadata.prerequisites.append(prerequisite)
        db.commit()
        db.refresh(taskmetadata)
        return taskmetadata

    def create(self, db: Session, *, taskmetadata: TaskMetadataCreate) -> TaskMetadata:
        db_obj = TaskMetadata(
            name_translations=taskmetadata.name_translations,
            description_translations=taskmetadata.description_translations,
            objectivemetadata_id=taskmetadata.objectivemetadata_id,
        )

        for id in taskmetadata.problem_profiles:
            if pp := problemprofilesCrud.get(db=db, id=id):
                db_obj.problemprofiles.append(pp)

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


tasksExportCrud = CRUDTaskMetadata(TaskMetadata)

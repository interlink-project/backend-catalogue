import uuid
from datetime import datetime
from typing import Any, List, Optional

from app.general.utils.AllOptional import AllOptional
from pydantic import BaseModel, validator
import requests
from app.config import settings
from app.artefacts.schemas import ArtefactBase, ArtefactCreate, ArtefactORM, ArtefactOut

class CoproductionSchemaBase(ArtefactBase):
    pass
    
class CoproductionSchemaCreate(ArtefactCreate, CoproductionSchemaBase):
    pass

class CoproductionSchemaPatch(CoproductionSchemaCreate, metaclass=AllOptional):
    pass


class CoproductionSchema(ArtefactORM, CoproductionSchemaBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    
    name: str
    description: str

    class Config:
        orm_mode = True


class CoproductionSchemaOut(ArtefactOut, CoproductionSchema):
    pass


####


class PhaseMetadataBase(BaseModel):
    is_public: bool = True
    

class PhaseMetadataCreate(PhaseMetadataBase):
    coproductionschema_id: uuid.UUID
    name_translations: dict
    description_translations: dict


class PhaseMetadataPatch(PhaseMetadataBase, metaclass=AllOptional):
    name_translations: Optional[dict]
    description_translations: Optional[dict]


class PhaseMetadata(PhaseMetadataBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    name: str
    description: str

    class Config:
        orm_mode = True


class PhaseMetadataOut(PhaseMetadata):
    pass

###

class ObjectiveMetadataBase(BaseModel):
    pass

class ObjectiveMetadataCreate(ObjectiveMetadataBase):
    phasemetadata_id: uuid.UUID
    name_translations: dict
    description_translations: dict


class ObjectiveMetadataPatch(ObjectiveMetadataBase):
    name_translations: Optional[dict]
    description_translations: Optional[dict]


class ObjectiveMetadata(ObjectiveMetadataBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    
    name: str
    description: str

    class Config:
        orm_mode = True


class ObjectiveMetadataOut(ObjectiveMetadata):
    pass

#####

class TaskMetadataBase(BaseModel):
    pass

class TaskMetadataCreate(TaskMetadataBase):
    objectivemetadata_id: uuid.UUID
    problemprofiles: list
    name_translations: dict
    description_translations: dict

class TaskMetadataPatch(TaskMetadataBase):
    problemprofiles: Optional[list]

    name_translations: Optional[dict]
    description_translations: Optional[dict]

class TaskMetadata(TaskMetadataBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    name: str
    description: str
    
    class Config:
        orm_mode = True


class TaskMetadataOut(TaskMetadata):
    # parent
    pass
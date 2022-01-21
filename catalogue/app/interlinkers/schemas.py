import uuid
from datetime import datetime
from typing import List, Optional, Union, Literal

from pydantic_choices import choice
from pydantic import BaseModel as PydanticBaseModel

from app.artefacts.schemas import ArtefactBase, ArtefactCreate, ArtefactORM, ArtefactOut
from app.general.utils.AllOptional import AllOptional
from typing_extensions import Annotated
from pydantic import Field
from pydantic import BaseModel
# Interlinker

NATURES = [("SoftwareInterlinker", "SOFTWARE"), ("KnowledgeInterlinker", "KNOWLEDGE")]

SOFTWARE_IMPLEMENTATIONS = [
    ("OS", "OPEN SOURCE"),
    ("OP", "ON PREMISES"),
    ("SA", "SAAS"),
]

SOFTWARE_TYPES = [
    ("IM", "IMPLEMENTATION"),
    ("SP", "SUPPORT"),
]

KNOWLEDGE_TYPES = [
    ("IM", "IMPLEMENTATION"),
    ("SP", "SUPPORT"),
]

natures = choice([key for key, value in NATURES])
sw_implementations = choice([key for key, value in SOFTWARE_IMPLEMENTATIONS])
sw_types = choice([key for key, value in SOFTWARE_TYPES])
kn_types = choice([key for key, value in KNOWLEDGE_TYPES])


class BaseInterlinkerBase(ArtefactBase):
    constraints: Optional[List[str]]
    regulations: Optional[List[str]]


class BaseInterlinkerCreate(ArtefactCreate, BaseInterlinkerBase):
    pass


class BaseInterlinkerPatch(BaseInterlinkerCreate, metaclass=AllOptional):
    pass


class BaseInterlinkerORM(ArtefactORM, BaseInterlinkerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class BaseInterlinkerOut(ArtefactOut, BaseInterlinkerORM):
    pass


###

class SoftwareBaseInterlinkerBase(BaseInterlinkerBase):
    nature: Literal["softwareinterlinker"]
    backend: str
    assets_deletable: bool
    assets_updatable: bool
    assets_clonable: bool
    


class SoftwareInterlinkerCreate(BaseInterlinkerCreate, SoftwareBaseInterlinkerBase):
    assets_deletable: Optional[bool]
    assets_updatable: Optional[bool]
    assets_clonable: Optional[bool]


class SoftwareInterlinkerPatch(SoftwareInterlinkerCreate, metaclass=AllOptional):
    pass


class SoftwareBaseInterlinkerORM(BaseInterlinkerORM, SoftwareBaseInterlinkerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class SoftwareInterlinkerOut(BaseInterlinkerOut, SoftwareBaseInterlinkerORM):
    # status: str
    pass


class BasicSoftwareInterlinkerOut(PydanticBaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    name: str
    backend: str
    # status: str
    
    class Config:
        orm_mode = True
### 

class KnowledgeBaseInterlinkerBase(BaseInterlinkerBase):
    nature: Literal["knowledgeinterlinker"]
    softwareinterlinker_id: uuid.UUID
    genesis_asset_id: Optional[str]


class KnowledgeInterlinkerCreate(BaseInterlinkerCreate, KnowledgeBaseInterlinkerBase):
    pass


class KnowledgeInterlinkerPatch(KnowledgeInterlinkerCreate, metaclass=AllOptional):
    pass


class KnowledgeBaseInterlinkerORM(BaseInterlinkerORM, KnowledgeBaseInterlinkerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class KnowledgeInterlinkerOut(BaseInterlinkerOut, KnowledgeBaseInterlinkerORM):
    softwareinterlinker: BasicSoftwareInterlinkerOut

InterlinkerCreate = Annotated[
    Union[KnowledgeInterlinkerCreate, SoftwareInterlinkerCreate],
    Field(discriminator="nature"),
]

InterlinkerPatch = Annotated[
    Union[KnowledgeInterlinkerPatch, SoftwareInterlinkerPatch],
    Field(discriminator="nature"),
]


class InterlinkerOut(BaseModel):
    __root__: Annotated[
        Union[KnowledgeInterlinkerOut, SoftwareInterlinkerOut],
        Field(discriminator="nature"),
    ]

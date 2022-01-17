import uuid
from datetime import datetime
from typing import List, Optional, Union, Literal

from pydantic_choices import choice

from app.artefacts.schemas import ArtefactBase, ArtefactCreate, ArtefactORM, ArtefactOut
from app.general.utils.AllOptional import AllOptional
from typing_extensions import Annotated
from pydantic import Field
from pydantic import BaseModel
from app.interlinkers.models import SOFTWARE_INTERLINKER_LITERAL, KNOWLEDGE_INTERLINKER_LITERAL
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
    backend: str


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
    nature: Literal[SOFTWARE_INTERLINKER_LITERAL]
    type: sw_types
    implementation: Optional[str]


class SoftwareInterlinkerCreate(BaseInterlinkerCreate, SoftwareBaseInterlinkerBase):
    pass


class SoftwareInterlinkerPatch(SoftwareInterlinkerCreate, metaclass=AllOptional):
    pass


class SoftwareBaseInterlinkerORM(BaseInterlinkerORM, SoftwareBaseInterlinkerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class SoftwareInterlinkerOut(BaseInterlinkerOut, SoftwareBaseInterlinkerORM):
    pass


### 

class KnowledgeBaseInterlinkerBase(BaseInterlinkerBase):
    nature: Literal[KNOWLEDGE_INTERLINKER_LITERAL]
    type: Optional[str]
    format: Optional[str]
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
    pass


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

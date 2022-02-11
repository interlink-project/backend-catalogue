import uuid
from datetime import datetime
from typing import List, Optional, Union, Literal
from enum import Enum

from pydantic_choices import choice
from pydantic import BaseModel as PydanticBaseModel

from app.artefacts.schemas import ArtefactBase, ArtefactCreate, ArtefactORM, ArtefactOut
from app.general.utils.AllOptional import AllOptional
from typing_extensions import Annotated
from pydantic import Field
from pydantic import BaseModel
from app.representations.schemas import RepresentationOut

# Interlinker

Difficulties = choice(["very_easy", "easy", "medium", "difficult", "very_difficult"])
Licences = choice(["public_domain", "permissive", "copyleft",
                  "non_commercial", "propietary"])
Targets = choice(["all", "all;pas", "all;pas;public_servants", "all;pas;politicians", "all;businesses", "all;businesses;smes", "all;businesses;freelancers", "all;businesses;large_companies", "all;businesses;private_non_profit",
                  "all;citizens", "all;citizens;potential_end_users", "all;citizens;expert_citizens", "all;research_organizations", "all;research_organizations;universities", "all;research_organizations;other_research_entities"])
InterlinkerTypes = choice(["enabling_services", "enabling_services;implementing_software_and_artifacts", "enabling_services;operation_services",
                          "enhancing_services", "enhancing_services;onboarding_services", "enhancing_services;followup_services", "enhancing_services:external_experts"])
AdministrativeScopes = choice(["eu", "national", "local"])


class BaseInterlinkerBase(ArtefactBase):
    difficulty: Difficulties
    targets: Optional[List[Targets]]
    licence: Licences
    types: Optional[List[InterlinkerTypes]]
    related_interlinkers: Optional[List[str]]
    administrative_scopes: Optional[List[AdministrativeScopes]]
    domain: Optional[str]
    process: Optional[str]

class BaseInterlinkerCreate(ArtefactCreate, BaseInterlinkerBase):
    constraints_and_limitations_translations: Optional[dict]
    regulations_and_standards_translations: Optional[dict]

class BaseInterlinkerPatch(BaseInterlinkerCreate, metaclass=AllOptional):
    pass


class BaseInterlinkerORM(ArtefactORM, BaseInterlinkerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class BaseInterlinkerOut(ArtefactOut, BaseInterlinkerORM):
    constraints_and_limitations: Optional[str]
    regulations_and_standards: Optional[str]



###

Supporters = choice(["saas", "on_premise", "installed_app"])
AuthMethods = choice(["header", "cookie"])

class SoftwareBaseInterlinkerBase(BaseInterlinkerBase):
    nature: Literal["softwareinterlinker"]

    supported_by: Supporters
    auth_method: AuthMethods
    deployment_manual: Optional[str]
    user_manual: Optional[str]
    developer_manual: Optional[str]

    supports_internationalization: bool

    is_responsive: bool
    # GUI is responsive
    open_in_modal: bool
    # assets for specific interlinkers may be opened on a modal, not in a new tab
    assets_clonable: bool
    # exposes an /assets/{id}/clone/ API endpoint?

    path: str
    is_subdomain: bool


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
    backend: Optional[str]


class BasicSoftwareInterlinkerOut(PydanticBaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    name: str
    backend: Optional[str]
    # status: str

    class Config:
        orm_mode = True

### 


class KnowledgeBaseInterlinkerBase(BaseInterlinkerBase):
    nature: Literal["knowledgeinterlinker"]
    instructions: str


class KnowledgeInterlinkerCreate(BaseInterlinkerCreate, KnowledgeBaseInterlinkerBase):
    pass


class KnowledgeInterlinkerPatch(KnowledgeInterlinkerCreate, metaclass=AllOptional):
    pass


class KnowledgeBaseInterlinkerORM(BaseInterlinkerORM, KnowledgeBaseInterlinkerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    representations: List[RepresentationOut]
    representations_count: int
    
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

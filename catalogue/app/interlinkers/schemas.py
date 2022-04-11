import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, validator
from pydantic_choices import choice
from typing_extensions import Annotated

from app.artefacts.schemas import ArtefactBase, ArtefactCreate, ArtefactORM, ArtefactOut
from app.config import settings
from app.general.utils.AllOptional import AllOptional
from app.integrations.schemas import IntegrationOut

from .models import Supporters

# Interlinker


Difficulties = choice(["very_easy", "easy", "medium", "difficult", "very_difficult"])

Targets = choice(["all", "all;pas", "all;pas;public_servants", "all;pas;politicians", "all;businesses", "all;businesses;smes", "all;businesses;freelancers", "all;businesses;large_companies", "all;businesses;private_non_profit",
                  "all;citizens", "all;citizens;potential_end_users", "all;citizens;expert_citizens", "all;research_organizations", "all;research_organizations;universities", "all;research_organizations;other_research_entities"])
InterlinkerTypes = choice(["enabling_services", "enabling_services;implementing_software_and_artifacts", "enabling_services;operation_services",
                          "enhancing_services", "enhancing_services;onboarding_services", "enhancing_services;followup_services", "enhancing_services:external_experts"])
AdministrativeScopes = choice(["eu", "national", "local"])

# kn
FormTypes = choice(["visual_template", "document_template", "canvas", "best_practices",
                   "guidelines", "checklist", "survey_template", "legal_agreement_template", "other"])
Formats = choice(["pdf", "editable_source_document",
                 "open_document", "structured_format"])


class BaseInterlinkerBase(ArtefactBase):
    languages: list = ["en"]
    published: Optional[bool]
    difficulty: Difficulties
    targets: Optional[List[Targets]]
    
    types: Optional[List[InterlinkerTypes]]
    administrative_scopes: Optional[List[AdministrativeScopes]]
    # domain: Optional[str]
    process: Optional[str]

    form: Optional[FormTypes]
    format: Optional[Formats]


class BaseInterlinkerCreate(ArtefactCreate, BaseInterlinkerBase):
    logotype: Optional[str]
    snapshots: Optional[List[str]]
    instructions_translations: dict

class BaseInterlinkerPatch(BaseInterlinkerCreate, metaclass=AllOptional):
    pass


class BaseInterlinkerORM(ArtefactORM, BaseInterlinkerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    instructions: str

    class Config:
        orm_mode = True


class BaseInterlinkerOut(ArtefactOut, BaseInterlinkerORM):
    logotype_link: Optional[str]
    snapshots_links: Optional[List[str]]
    related_interlinkers: Optional[List[str]]

###


class SoftwareBaseInterlinkerBase(BaseInterlinkerBase):
    nature: Literal["softwareinterlinker"] = "softwareinterlinker"
    supported_by: List[Supporters]
    supports_internationalization: bool
    is_responsive: bool
    # GUI is responsive


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
    integration: Optional[IntegrationOut]

# class BasicSoftwareInterlinkerOut(PydanticBaseModel):
#     id: uuid.UUID
#     created_at: datetime
#     updated_at: Optional[datetime]
#     name: str
#     backend: Optional[str]
#     # status: str
#
#     class Config:
#         orm_mode = True

### 


class KnowledgeBaseInterlinkerBase(BaseInterlinkerBase):
    nature: Literal["knowledgeinterlinker"] = "knowledgeinterlinker"
    softwareinterlinker_id: uuid.UUID
    parent_id: Optional[uuid.UUID]


class KnowledgeInterlinkerCreate(BaseInterlinkerCreate, KnowledgeBaseInterlinkerBase):
    genesis_asset_id_translations: Optional[dict]
    instructions_translations: dict


class KnowledgeInterlinkerPatch(KnowledgeInterlinkerCreate, metaclass=AllOptional):
    pass


class KnowledgeBaseInterlinkerORM(BaseInterlinkerORM, KnowledgeBaseInterlinkerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    genesis_asset_id: str
    
    class Config:
        orm_mode = True


class BasicKnowledgeInterlinker(BaseInterlinkerOut, KnowledgeBaseInterlinkerORM):
    link: str
    internal_link: str


class KnowledgeInterlinkerOut(BasicKnowledgeInterlinker, KnowledgeBaseInterlinkerORM):
    softwareinterlinker: Optional[SoftwareInterlinkerOut]
    children: List[BasicKnowledgeInterlinker]


### ExternalInterlinker


class ExternalBaseInterlinkerBase(BaseInterlinkerBase):
    nature: Literal["externalinterlinker"] = "externalinterlinker"
    type: str
    


class ExternalInterlinkerCreate(BaseInterlinkerCreate, ExternalBaseInterlinkerBase):
    uri_translations: dict
    asset_name_translations: Optional[dict]


class ExternalInterlinkerPatch(ExternalInterlinkerCreate, metaclass=AllOptional):
    pass


class ExternalBaseInterlinkerORM(BaseInterlinkerORM, ExternalBaseInterlinkerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    uri: str
    asset_name: Optional[str]

    class Config:
        orm_mode = True


class BasicExternalInterlinker(BaseInterlinkerOut, ExternalBaseInterlinkerORM):
    pass


class ExternalInterlinkerOut(BasicExternalInterlinker, ExternalBaseInterlinkerORM):
    pass


InterlinkerCreate = Annotated[
    Union[SoftwareInterlinkerCreate, KnowledgeInterlinkerCreate, ExternalInterlinkerCreate],
    Field(discriminator="nature"),
]

InterlinkerPatch = Annotated[
    Union[SoftwareInterlinkerPatch, KnowledgeInterlinkerPatch, ExternalInterlinkerPatch],
    Field(discriminator="nature"),
]


class InterlinkerOut(BaseModel):
    __root__: Annotated[
        Union[SoftwareInterlinkerOut, KnowledgeInterlinkerOut, ExternalInterlinkerOut],
        Field(discriminator="nature"),
    ]

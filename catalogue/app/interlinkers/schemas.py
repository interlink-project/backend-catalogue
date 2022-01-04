import uuid
from datetime import datetime
from typing import List, Optional

from app.problemdomains.schemas import (
    ProblemDomainBase,
    ProblemDomainCreate,
    ProblemDomainOut,
)
from app.general.utils.AllOptional import AllOptional
from pydantic import BaseModel
from pydantic_choices import choice
from app.artefacts.schemas import (
    ArtefactBase,
    ArtefactCreate,
    ArtefactORM,
    ArtefactOut,
)
# Interlinker

TYPES = [("A11", "easfas"), ("A12", "ADFSSADF")]

NATURES = [("SW", "SOFTWARE"), ("KN", "KNOWLEDGE")]

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

types = choice([key for key, value in TYPES])
natures = choice([key for key, value in NATURES])
sw_implementations = choice([key for key, value in SOFTWARE_IMPLEMENTATIONS])
sw_types = choice([key for key, value in SOFTWARE_TYPES])
kn_types = choice([key for key, value in KNOWLEDGE_TYPES])


class InterlinkerBase(ArtefactBase):
    SOC_type: types
    nature: natures

    administrative_scope: Optional[str]
    specific_app_domain: Optional[List[str]]
    constraints: Optional[List[str]]
    regulations: Optional[List[str]]
    software_type: Optional[sw_types]
    software_implementation: Optional[sw_implementations]
    software_customization: Optional[str]
    software_integration: Optional[str]
    knowledge_type: Optional[kn_types]
    knowledge_format: Optional[str]

    backend: str
    init_asset_id: Optional[str]

class InterlinkerCreate(ArtefactCreate, InterlinkerBase):
    pass


class InterlinkerPatch(InterlinkerCreate, metaclass=AllOptional):
    pass


class InterlinkerORM(ArtefactORM, InterlinkerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class InterlinkerOut(ArtefactOut, InterlinkerORM):
    pass

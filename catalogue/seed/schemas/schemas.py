import enum
from typing import Dict, List, Optional, Union

from configuration import Environments, Languages, Complexities
from problemprofiles.problemprofiles import WithProblemProfiles
from pydantic import BaseModel, Extra, conlist, validator


class Licences(enum.Enum):
    public_domain = "public_domain"
    permissive = "permissive"
    copyleft = "copyleft"
    non_commercial = "non_commercial"
    propietary = "propietary"


class WithNameAndDesc(BaseModel):
    name_translations: dict
    description_translations: dict

    @validator('name_translations', "description_translations")
    def with_languages(cls, v, values, **kwargs):
        if "en" not in v:
            raise ValueError(f'English not detected')
        return v


class Task(WithProblemProfiles, WithNameAndDesc, extra=Extra.forbid):
    id: str
    prerequisites: Dict[str, str]
    complexity: Optional[List[Complexities]]
    
    # Changed for the list of complexities above
    # management: Optional[int]
    # development: Optional[int]
    # exploitation: Optional[int]


class Objective(WithProblemProfiles, WithNameAndDesc, extra=Extra.forbid):
    id: str
    prerequisites: Dict[str, str]
    tasks: List[Task]


class Phase(WithNameAndDesc, extra=Extra.forbid):
    id: str
    prerequisites: Dict[str, str]
    objectives: List[Objective]
    is_part_of_codelivery: bool


class CoproductionSchema(WithNameAndDesc, extra=Extra.forbid):
    id: str
    tags_translations: Dict[str,  conlist(str, min_items=1)]
    author: str
    licence: Licences
    languages: Optional[List[Languages]]
    environments: Optional[List[Environments]]

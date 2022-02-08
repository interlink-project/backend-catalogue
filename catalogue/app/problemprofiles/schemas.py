from datetime import datetime
from typing import List, Optional

from app.general.utils.AllOptional import AllOptional
from pydantic import BaseModel

class ProblemProfileBase(BaseModel):
    id: str
    

class ProblemProfileCreate(ProblemProfileBase):
    name_translations: dict
    description_translations: dict
    functionality_translations: dict


class ProblemProfilePatch(ProblemProfileCreate, metaclass=AllOptional):
    pass

class ProblemProfile(ProblemProfileBase):
    name: str
    description: str
    functionality: str

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ProblemProfileOut(ProblemProfile):
    pass
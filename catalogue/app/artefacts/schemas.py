import uuid
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel as PydanticBaseModel, validator

class ArtefactBase(PydanticBaseModel):
    pass


class ArtefactCreate(ArtefactBase):
    problemprofiles: List[str] = []
    name_translations: Dict[str, str]
    description_translations: Dict[str, str]
    constraints_and_limitations_translations: Optional[Dict[str, str]]
    regulations_and_standards_translations: Optional[Dict[str, str]]
    tags_translations: Dict[str, str]
    creator_id: Optional[uuid.UUID]

    @validator('tags_translations', pre=True)
    def swith_array_to_str(cls, v):
        if v:
            return { key: ";".join(value) for key, value in v.items()}
        return v

class ArtefactORM(ArtefactBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    name: str
    description: str
    constraints_and_limitations: Optional[str]
    regulations_and_standards: Optional[str]

    rating: Optional[float]
    ratings_count: Optional[int]
    
    class Config:
        orm_mode = True

class ProblemProfile(PydanticBaseModel):
    id: str
    name: str
    description: str
    
    class Config:
        orm_mode = True
        
class ArtefactOut(ArtefactORM):
    artefact_type: str
    problemprofiles: List[ProblemProfile]
    tags: list
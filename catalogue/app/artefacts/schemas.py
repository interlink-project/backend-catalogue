import uuid
from typing import List, Optional
from datetime import datetime

from pydantic import validator, BaseModel as PydanticBaseModel
from app.problemprofiles.schemas import ProblemProfileOut
from app.questioncomments.schemas import QuestionCommentOut
from app.config import settings

class ArtefactBase(PydanticBaseModel):
    logotype: Optional[str]
    published: Optional[bool]
    tags: List[str]
    snapshots: Optional[List[str]]

class ArtefactCreate(ArtefactBase):
    problem_profiles: Optional[List[str]]
    name_translations: dict
    description_translations: dict

class ArtefactORM(ArtefactBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    
    name: str
    description: str

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

    @validator('logotype', pre=True)
    def set_logotype(cls, v):
        if v:
            return settings.COMPLETE_SERVER_NAME + v
        return v
        
    @validator('snapshots', pre=True)
    def set_snapshots(cls, v):
        if v and type(v) == list:
            new = []
            for i in v:
                new.append(settings.COMPLETE_SERVER_NAME + i) 
            return new
        return v
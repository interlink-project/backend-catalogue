import uuid
from datetime import datetime
from typing import Optional

from app.artefacts.schemas import ArtefactBase, ArtefactCreate, ArtefactORM, ArtefactOut
from app.general.utils.AllOptional import AllOptional


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

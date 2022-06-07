import uuid
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, validator
from .models import TreeItemTypes

class TreeItemBase(BaseModel):
    name_translations: dict
    description_translations: dict
    coproductionschema_id: Optional[uuid.UUID]
    parent_id: Optional[uuid.UUID]
    type: TreeItemTypes
    problemprofiles: Optional[list]

class TreeItemCreate(TreeItemBase):
    pass    

class TreeItemPatch(TreeItemBase):
    pass

class TreeItem(TreeItemBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    name: str
    description: str

    class Config:
        orm_mode = True


class TreeItemOut(TreeItem):
    children_ids: List[uuid.UUID]
    prerequisites_ids: List[uuid.UUID]

    @validator('prerequisites_ids', pre=True)
    def prerequisites_ids_to_list(cls, v):
        return list(v)

    @validator('children_ids', pre=True)
    def children_ids_to_list(cls, v):
        return list(v)

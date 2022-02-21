import uuid
from datetime import datetime
from typing import List, Optional
from app.general.utils.AllOptional import AllOptional
from pydantic import BaseModel, validator
from pydantic.typing import ForwardRef
from pydantic_choices import choice


AuthMethods = choice(["header", "cookie"])


class IntegrationBase(BaseModel):
    softwareinterlinker_id: uuid.UUID
    auth_method: AuthMethods

    # endpoint
    service_name: str
    domain: str
    path: str
    is_subdomain: bool
    api_path: str

    # capabilities
    instantiate: bool
    clone: bool
    view: bool
    edit: bool
    delete: bool
    open_in_modal: bool
    shortcut: bool


class IntegrationCreate(IntegrationBase):
    pass


class IntegrationPatch(IntegrationCreate, metaclass=AllOptional):
    pass


class Integration(IntegrationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class IntegrationOut(Integration):
    pass

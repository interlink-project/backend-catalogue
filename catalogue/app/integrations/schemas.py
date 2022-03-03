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
    # capabilities translations
    instantiate_text_translations: Optional[dict]
    view_text_translations: Optional[dict]
    edit_text_translations: Optional[dict]
    delete_text_translations: Optional[dict]
    clone_text_translations: Optional[dict]


class IntegrationPatch(IntegrationCreate, metaclass=AllOptional):
    pass


class Integration(IntegrationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    instantiate_text: Optional[str]
    view_text: Optional[str]
    clone_text: Optional[str]
    edit_text: Optional[str]
    delete_text: Optional[str]

    class Config:
        orm_mode = True


class IntegrationOut(Integration):
    pass

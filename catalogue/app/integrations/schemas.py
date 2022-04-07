import uuid
from datetime import datetime
from typing import Optional
from app.general.utils.AllOptional import AllOptional
from pydantic import BaseModel
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
    instantiate: Optional[bool]
    clone: Optional[bool]
    view: Optional[bool]
    edit: Optional[bool]
    delete: Optional[bool]
    download: Optional[bool]
    preview: Optional[bool]
    open_in_modal: Optional[bool]
    shortcut: Optional[bool]


class IntegrationCreate(IntegrationBase):
    # capabilities translations
    instantiate_text_translations: Optional[dict]
    view_text_translations: Optional[dict]
    edit_text_translations: Optional[dict]
    delete_text_translations: Optional[dict]
    clone_text_translations: Optional[dict]
    download_text_translations: Optional[dict]
    preview_text_translations: Optional[dict]


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
    preview_text: Optional[str]

    class Config:
        orm_mode = True


class IntegrationOut(Integration):
    pass


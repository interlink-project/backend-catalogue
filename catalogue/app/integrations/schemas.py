import uuid
from datetime import datetime
from typing import List, Literal, Optional
from app.general.utils.AllOptional import AllOptional
from pydantic import BaseModel, validator, Field
from pydantic.typing import ForwardRef, Union
from pydantic_choices import choice
from typing_extensions import Annotated

AuthMethods = choice(["header", "cookie"])


class InternalIntegrationBase(BaseModel):
    type: Literal["internalintegration"] = "internalintegration"

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
    download: bool
    open_in_modal: bool
    shortcut: bool


class InternalIntegrationCreate(InternalIntegrationBase):
    # capabilities translations
    instantiate_text_translations: Optional[dict]
    view_text_translations: Optional[dict]
    edit_text_translations: Optional[dict]
    delete_text_translations: Optional[dict]
    clone_text_translations: Optional[dict]
    download_text_translations: Optional[dict]


class InternalIntegrationPatch(InternalIntegrationCreate, metaclass=AllOptional):
    pass


class InternalIntegration(InternalIntegrationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    instantiate_text: Optional[str]
    view_text: Optional[str]
    clone_text: Optional[str]
    edit_text: Optional[str]
    delete_text: Optional[str]
    download_text: Optional[str]

    class Config:
        orm_mode = True


class InternalIntegrationOut(InternalIntegration):
    pass


## EXTERNAL


class ExternalIntegrationBase(BaseModel):
    type: Literal["externalintegration"] = "externalintegration"
    softwareinterlinker_id: uuid.UUID
    result_softwareinterlinker_id: Optional[uuid.UUID]
    redirection: str


class ExternalIntegrationCreate(ExternalIntegrationBase):
    pass


class ExternalIntegrationPatch(ExternalIntegrationCreate, metaclass=AllOptional):
    pass


class ExternalIntegration(ExternalIntegrationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    pass

    class Config:
        orm_mode = True


class ExternalIntegrationOut(ExternalIntegration):
    pass


IntegrationCreate = Annotated[
    Union[InternalIntegrationCreate, ExternalIntegrationCreate],
    Field(discriminator="type"),
]

IntegrationPatch = Annotated[
    Union[InternalIntegrationPatch, ExternalIntegrationPatch],
    Field(discriminator="type"),
]


class IntegrationOut(BaseModel):
    __root__: Annotated[
        Union[InternalIntegrationOut, ExternalIntegrationOut],
        Field(discriminator="type"),
    ]

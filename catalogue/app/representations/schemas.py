import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic_choices import choice

from app.general.utils.AllOptional import AllOptional

FormTypes = choice(["visual_template", "document_template", "canvas", "best_practices",
                   "guidelines", "checklist", "survey_template", "legal_agreement_template", "other"])
Formats = choice(["pdf", "editable_source_document",
                 "open_document", "structured_format"])


class RepresentationBase(BaseModel):
    softwareinterlinker_id: uuid.UUID
    genesis_asset_id: str
    form: FormTypes
    format: Formats

class RepresentationCreate(RepresentationBase):
    knowledgeinterlinker_id: uuid.UUID


class RepresentationPatch(RepresentationCreate, metaclass=AllOptional):
    pass


class Representation(RepresentationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class RepresentationOut(Representation):
    pass

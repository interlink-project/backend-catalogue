import uuid
from datetime import datetime

from app.general.db.base_class import Base as BaseModel
from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import HSTORE
from app.locales import translation_hybrid


class Integration(BaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String)

    softwareinterlinker_id = Column(UUID(as_uuid=True), ForeignKey("softwareinterlinker.id"))
    softwareinterlinker = relationship("SoftwareInterlinker", back_populates="integration", foreign_keys=[softwareinterlinker_id])

    service_name = Column(String)
    domain = Column(String)
    path = Column(String)
    is_subdomain = Column(Boolean, default=False)
    api_path = Column(String)
    auth_method = Column(String)

    # capabilities
    instantiate = Column(Boolean, default=False)
    view = Column(Boolean, default=False)
    edit = Column(Boolean, default=False)
    clone = Column(Boolean, default=False)
    delete = Column(Boolean, default=False)
    download = Column(Boolean, default=False)
    preview = Column(Boolean, default=False)
    open_in_modal = Column(Boolean, default=False)
    shortcut = Column(Boolean, default=False)
    
    # capabilities translations
    instantiate_text_translations = Column(HSTORE)
    view_text_translations = Column(HSTORE)
    edit_text_translations = Column(HSTORE)
    delete_text_translations = Column(HSTORE)
    clone_text_translations = Column(HSTORE)
    download_text_translations = Column(HSTORE)
    preview_text_translations = Column(HSTORE)

    instantiate_text = translation_hybrid(instantiate_text_translations)
    view_text = translation_hybrid(view_text_translations)
    clone_text = translation_hybrid(clone_text_translations)
    edit_text = translation_hybrid(edit_text_translations)
    delete_text = translation_hybrid(delete_text_translations)
    download_text = translation_hybrid(download_text_translations)
    preview_text = translation_hybrid(preview_text_translations)

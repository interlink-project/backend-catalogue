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


class Integration(BaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    softwareinterlinker_id = Column(UUID(as_uuid=True), ForeignKey("softwareinterlinker.id"))
    softwareinterlinker = relationship("SoftwareInterlinker", back_populates="integration")

    service_name = Column(String)
    domain = Column(String)
    path = Column(String)
    is_subdomain = Column(Boolean, default=False)
    api_path = Column(String)
    auth_method = Column(String)

    # capabilities
    clone = Column(Boolean, default=False)
    instantiate = Column(Boolean, default=True)
    view = Column(Boolean, default=True)
    edit = Column(Boolean, default=False)
    delete = Column(Boolean, default=True)
    open_in_modal = Column(Boolean, default=False)
    shortcut = Column(Boolean, default=False)
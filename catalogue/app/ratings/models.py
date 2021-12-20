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


class Rating(BaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    artefact_id = Column(UUID(as_uuid=True), ForeignKey("artefact.id"))
    artefact = relationship("Artefact", back_populates="ratings")
    user_id = Column(UUID(as_uuid=True))
    value = Column(Integer)
    title = Column(String, nullable=True)
    text = Column(Text)

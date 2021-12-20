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
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.artefacts.models import Artefact
import uuid


class PublicService(Artefact):
    id = Column(
        UUID(as_uuid=True),
        ForeignKey("artefact.id"),
        primary_key=True,
        default=uuid.uuid4,
    )
    language = Column(String, nullable=True)
    processing_time = Column(String, nullable=True)
    location = Column(String, nullable=True)
    status = Column(String, nullable=True)
    public_organization = Column(String, nullable=True)
    output = Column(String, nullable=True)
    cost = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "publicservice",
    }

    def __repr__(self) -> str:
        return f"<PublicService {self.name}>"

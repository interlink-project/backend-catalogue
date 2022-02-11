import uuid
from datetime import datetime

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
    event,
)
from sqlalchemy.dialects.postgresql import HSTORE, UUID
from sqlalchemy.orm import relationship

from app.general.db.base_class import Base as BaseModel
from app.tables import artefact_problem_association_table
from app.translations import translation_hybrid


class Artefact(BaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artefact_type = Column(String(70))

    name_translations = Column(HSTORE)
    description_translations = Column(HSTORE, nullable=True)

    name = translation_hybrid(name_translations)
    description = translation_hybrid(description_translations)

    published = Column(Boolean, default=False)
    logotype = Column(String, nullable=True)
    snapshots = Column(ARRAY(String), default=list)
    tags = Column(ARRAY(String), default=list)

    problemprofiles = relationship(
        "ProblemProfile",
        secondary=artefact_problem_association_table,
        back_populates="artefacts",
    )
    ratings = relationship("Rating", back_populates="artefact")
    questioncomments = relationship("QuestionComment", back_populates="artefact")

    __mapper_args__ = {
        "polymorphic_identity": "artefact",
        "polymorphic_on": artefact_type,
    }

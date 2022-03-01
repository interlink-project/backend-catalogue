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
    constraints_and_limitations_translations = Column(HSTORE)
    regulations_and_standards_translations = Column(HSTORE, nullable=True)
    tags_translations = Column(HSTORE)

    name = translation_hybrid(name_translations)
    description = translation_hybrid(description_translations)
    constraints_and_limitations = translation_hybrid(constraints_and_limitations_translations)
    regulations_and_standards = translation_hybrid(regulations_and_standards_translations)
    tags = translation_hybrid(tags_translations)
    
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

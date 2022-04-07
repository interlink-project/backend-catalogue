import uuid
from datetime import datetime

from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    event,
)
from sqlalchemy.dialects.postgresql import HSTORE, UUID
from sqlalchemy.orm import relationship

from app.general.db.base_class import Base as BaseModel
from app.tables import artefact_problem_association_table
from app.middleware import translation_hybrid
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from sqlalchemy_utils import aggregated

from app.ratings.models import Rating


class Artefact(BaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artefact_type = Column(String(70))

    is_public = Column(Boolean, default=False)
    licence = Column(String, nullable=True)

    name_translations = Column(HSTORE)
    description_translations = Column(HSTORE, nullable=True)
    constraints_and_limitations_translations = Column(HSTORE)
    regulations_and_standards_translations = Column(HSTORE, nullable=True)
    tags_translations = Column(HSTORE)

    name = translation_hybrid(name_translations)
    description = translation_hybrid(description_translations)
    constraints_and_limitations = translation_hybrid(constraints_and_limitations_translations)
    regulations_and_standards = translation_hybrid(regulations_and_standards_translations)
    _tags = translation_hybrid(tags_translations)
    
    problemprofiles = relationship(
        "ProblemProfile",
        secondary=artefact_problem_association_table,
        back_populates="artefacts",
    )

    # 1 digit for decimals
    @aggregated('ratings', Column(Numeric(2, 1), default=0))
    def rating(self):
        return func.avg(Rating.value)
    
    @aggregated('ratings', Column(Integer, default=0))
    def ratings_count(self):
        return func.count('1')

    ratings = relationship("Rating", back_populates="artefact")
    questioncomments = relationship("QuestionComment", back_populates="artefact")

    # TODO: creator type: team or user
    creator_id = Column(UUID(as_uuid=True), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "artefact",
        "polymorphic_on": artefact_type,
    }

    @hybrid_property
    def tags(self):
        # can not store arrays on hstore, so stored in string and splitted in get
        return self._tags.split(";")
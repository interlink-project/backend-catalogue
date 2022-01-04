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
from app.tables import (
    artefact_problem_association_table,
    artefact_functionality_association_table,
)


class Artefact(BaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artefact_type = Column(String(70))

    name = Column(String)
    description = Column(String)
    published = Column(Boolean, default=False)
    logotype = Column(String)
    keywords = Column(ARRAY(String))
    documentation = Column(String, nullable=True)
    
    problemdomains = relationship(
        "ProblemDomain",
        secondary=artefact_problem_association_table,
        back_populates="artefacts",
    )
    functionalities = relationship(
        "Functionality",
        secondary=artefact_functionality_association_table,
        back_populates="artefacts",
    )
    #
    ratings = relationship("Rating", back_populates="artefact")
    questioncomments = relationship("QuestionComment", back_populates="artefact")

    __mapper_args__ = {
        "polymorphic_identity": "artefact",
        "polymorphic_on": artefact_type,
    }

from app.general.db.base_class import Base as BaseModel
from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Table,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.tables import (
    problem_functionality_association_table,
    artefact_functionality_association_table,
)
import uuid

class Functionality(BaseModel):
    """
    Defines the functionalities model
    """
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    problemdomains = relationship(
        "ProblemDomain",
        secondary=problem_functionality_association_table,
        back_populates="functionalities",
    )
    artefacts = relationship(
        "Artefact",
        secondary=artefact_functionality_association_table,
        back_populates="functionalities",
    )

    def __repr__(self) -> str:
        return f"<Functionality {self.name}>"

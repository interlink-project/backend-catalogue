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
    artefact_problem_association_table,
)
import uuid

class ProblemDomain(BaseModel):
    """
    Defines the problemdomains model
    """
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String)
    target_stakeholder_groups = Column(ARRAY(String))
    description = Column(String)
    functionalities = relationship(
        "Functionality",
        secondary=problem_functionality_association_table,
        back_populates="problemdomains",
    )
    artefacts = relationship(
        "Artefact",
        secondary=artefact_problem_association_table,
        back_populates="problemdomains",
    )

    def __repr__(self) -> str:
        return f"<ProblemDomain {self.name}>"

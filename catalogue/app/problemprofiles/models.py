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
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.orm import relationship

from app.general.db.base_class import Base as BaseModel
from app.tables import artefact_problem_association_table
from app.translations import translation_hybrid


class ProblemProfile(BaseModel):
    """
    Defines the problemprofiles model
    """
    id = Column(String, primary_key=True)
    name_translations = Column(HSTORE)
    description_translations = Column(HSTORE)
    functionality_translations = Column(HSTORE)

    name = translation_hybrid(name_translations)
    description = translation_hybrid(description_translations)
    functionality = translation_hybrid(description_translations)

    artefacts = relationship(
        "Artefact",
        secondary=artefact_problem_association_table,
        back_populates="problemprofiles",
    )

    def __repr__(self) -> str:
        return f"<ProblemProfile {self.name}>"

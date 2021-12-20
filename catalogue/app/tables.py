from app.general.db.base_class import Base as BaseModel
from sqlalchemy import Table, ForeignKey, Column

problem_functionality_association_table = Table(
    "problem_functionalities",
    BaseModel.metadata,
    Column("functionality_id", ForeignKey("functionality.id")),
    Column("problemdomain_id", ForeignKey("problemdomain.id")),
)

artefact_functionality_association_table = Table(
    "artefact_functionality",
    BaseModel.metadata,
    Column("functionality_id", ForeignKey("functionality.id")),
    Column("artefact_id", ForeignKey("artefact.id")),
)

artefact_problem_association_table = Table(
    "artefact_problem",
    BaseModel.metadata,
    Column("artefact_id", ForeignKey("artefact.id")),
    Column("problemdomain_id", ForeignKey("problemdomain.id")),
)

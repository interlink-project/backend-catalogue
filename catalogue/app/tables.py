from app.general.db.base_class import Base as BaseModel
from sqlalchemy import Table, ForeignKey, Column

artefact_problem_association_table = Table(
    "artefact_problem",
    BaseModel.metadata,
    Column("artefact_id", ForeignKey("artefact.id")),
    Column("problemprofile_id", ForeignKey("problemprofile.id")),
)
import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.artefacts.models import Artefact


class CoproductionSchema(Artefact):
    """
    Inherits from artefact (name, description, tags...)
    """
    id = Column(
        UUID(as_uuid=True),
        ForeignKey("artefact.id", ondelete="CASCADE"),
        primary_key=True,
        default=uuid.uuid4,
    )

    __mapper_args__ = {
        "polymorphic_identity": "coproductionschema",
    }

    def __repr__(self):
        return "<CoproductionSchema %r>" % self.name

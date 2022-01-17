import uuid
from typing import Union

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
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.utils import cached_property

from app.artefacts.models import Artefact

KNOWLEDGE_INTERLINKER_LITERAL: str = "knowledgeinterlinker"
SOFTWARE_INTERLINKER_LITERAL: str = "softwareinterlinker"

class Interlinker(Artefact):
    """
    Defines the interlinker model
    """
    id = Column(
        UUID(as_uuid=True),
        ForeignKey("artefact.id"),
        primary_key=True,
        default=uuid.uuid4,
    )
    nature = Column(String)
    constraints = Column(ARRAY(String), nullable=True)
    regulations = Column(ARRAY(String), nullable=True)
    # googledrive, forum...
    backend = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "interlinker",
        "polymorphic_on": nature,
    }

    def __repr__(self) -> str:
        return f"<Interlinker {self.name}>"

    @cached_property
    def is_knowledge(self):
        return self.nature == "KN"


class SoftwareInterlinker(Interlinker):
    """
    Defines the software interlinker model
    """
    id = Column(
        UUID(as_uuid=True),
        ForeignKey("interlinker.id"),
        primary_key=True,
        default=uuid.uuid4,
    )
    # SW or KN
    type = Column(String, nullable=True)
    # IM or SP
    implementation = Column(String, nullable=True)
    # OS, OP, SAAS

    __mapper_args__ = {
        "polymorphic_identity": SOFTWARE_INTERLINKER_LITERAL,
    }

    def __repr__(self) -> str:
        return f"<SoftwareInterlinker {self.name}>"


class KnowledgeInterlinker(Interlinker):
    """
    Defines the knowledge interlinker model
    """
    id = Column(
        UUID(as_uuid=True),
        ForeignKey("interlinker.id"),
        primary_key=True,
        default=uuid.uuid4,
    )

    type = Column(String, nullable=True)
    format = Column(String, nullable=True)
    genesis_asset_id = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": KNOWLEDGE_INTERLINKER_LITERAL,
    }

    def __repr__(self) -> str:
        return f"<KnowledgeInterlinker {self.name}>"


InterlinkerModel = Union[KnowledgeInterlinker, SoftwareInterlinker]

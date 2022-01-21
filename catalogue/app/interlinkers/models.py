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
from sqlalchemy.orm import relationship

from app.artefacts.models import Artefact

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

    # discriminator
    nature = Column(String)
    
    __mapper_args__ = {
        "polymorphic_identity": "interlinker",
        "polymorphic_on": nature,
    }

    def __repr__(self) -> str:
        return f"<Interlinker {self.name}>"

    @cached_property
    def is_knowledge(self):
        return self.nature == "knowledgeinterlinker"


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
    #knowledgeinterlinkers = relationship("KnowledgeInterlinker", back_populates="softwareinterlinker")
    # googledrive, forum...
    backend = Column(String)
    # has DELETE endpoint
    assets_deletable = Column(Boolean, default=False)
    # has /modify endpoint
    assets_updatable = Column(Boolean, default=False)
    # has /clone endpoint
    assets_clonable = Column(Boolean, default=False)

    status = Column(String, default="off")
    __mapper_args__ = {
        "polymorphic_identity": "softwareinterlinker",
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

    genesis_asset_id = Column(String, nullable=True)
    softwareinterlinker_id = Column(UUID(as_uuid=True), ForeignKey("softwareinterlinker.id"))
    softwareinterlinker = relationship("SoftwareInterlinker", backref='softwareinterlinker', foreign_keys=[softwareinterlinker_id])

    __mapper_args__ = {
        "polymorphic_identity": "knowledgeinterlinker",
    }

    def __repr__(self) -> str:
        return f"<KnowledgeInterlinker {self.name}>"

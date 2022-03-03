import enum
import uuid
from typing import Optional, Union

from pydantic_choices import choice
from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import HSTORE, UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship
from sqlalchemy_utils import aggregated

from app.artefacts.models import Artefact
from app.config import settings
from app.translations import translation_hybrid
from app.integrations.models import Integration


class Supporters(enum.Enum):
    saas = "saas"
    on_premise = "on_premise"
    installed_app = "installed_app"

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
    languages = Column(ARRAY(String), default=list)

    published = Column(Boolean, default=False)
    logotype = Column(String, nullable=True)
    snapshots = Column(ARRAY(String), default=list)

    difficulty = Column(String)
    targets = Column(ARRAY(String), default=list)
    licence = Column(String)
    types = Column(ARRAY(String), default=list)
    # related_interlinkers
    administrative_scopes = Column(ARRAY(String), default=list)
    # domain = Column(String, nullable=True)
    process = Column(String, nullable=True)

    # discriminator
    nature = Column(String)
    
    __mapper_args__ = {
        "polymorphic_identity": "interlinker",
        "polymorphic_on": nature,
    }

    @property
    def logotype_link(self):
        return settings.COMPLETE_SERVER_NAME + self.logotype if self.logotype else ""

    @property
    def snapshots_links(self):
        return [settings.COMPLETE_SERVER_NAME + i for i in self.snapshots] if self.snapshots else []

    def __repr__(self) -> str:
        return f"<Interlinker {self.id}>"

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

    supported_by = Column(
        ARRAY(Enum(Supporters, create_constraint=False, native_enum=False))
    )

    deployment_manual = Column(String, nullable=True)
    user_manual = Column(String, nullable=True)
    developer_manual = Column(String, nullable=True)
    supports_internationalization = Column(Boolean, default=False)
    is_responsive = Column(Boolean, default=False)
    
    integration = relationship("Integration", back_populates="softwareinterlinker", uselist=False)
    
    status = Column(String, default="off")
    __mapper_args__ = {
        "polymorphic_identity": "softwareinterlinker",
    }

    def __repr__(self) -> str:
        return f"<SoftwareInterlinker {self.id}>"

    @property
    def backend(self):
        if not self.integration or settings.DEVSOLOMODE:
            return None
        integration : Integration = self.integration
        SERVER_NAME = integration.domain or settings.SERVER_NAME
        if integration.is_subdomain:
            return f"{settings.PROTOCOL}{integration.path}.{SERVER_NAME}{integration.api_path}"
        return f"{settings.PROTOCOL}{SERVER_NAME}/{integration.path}{integration.api_path}"

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
    form = Column(String)
    format = Column(String)

    instructions_translations = Column(HSTORE)
    instructions = translation_hybrid(instructions_translations)

    softwareinterlinker_id = Column(UUID(as_uuid=True), ForeignKey("softwareinterlinker.id", ondelete='CASCADE'))
    softwareinterlinker = relationship("SoftwareInterlinker", backref='knowledgeinterlinkers', foreign_keys=[softwareinterlinker_id])
    
    genesis_asset_id_translations = Column(HSTORE)
    genesis_asset_id = translation_hybrid(genesis_asset_id_translations)
    
    parent_id = Column(UUID(as_uuid=True), ForeignKey("knowledgeinterlinker.id"))
    children = relationship(
        "KnowledgeInterlinker", backref=backref("parent", remote_side=[id]), foreign_keys=[parent_id]
    )
    __mapper_args__ = {
        "polymorphic_identity": "knowledgeinterlinker",
    }

    def __repr__(self) -> str:
        return f"<KnowledgeInterlinker {self.id}>"

    @property
    def link(self):
        return f"{self.softwareinterlinker.backend}/{self.genesis_asset_id}"

    # not exposed in out schema
    @property
    def internal_link(self):
        backend = self.softwareinterlinker.integration.service_name
        api_path = self.softwareinterlinker.integration.api_path
        return f"http://{backend}{api_path}/{self.genesis_asset_id}"
        
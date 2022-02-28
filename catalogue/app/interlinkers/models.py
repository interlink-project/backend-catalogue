import uuid
from typing import Union
import enum
from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum,
)
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.utils import cached_property
from sqlalchemy.orm import relationship
from app.config import settings
from app.artefacts.models import Artefact
from sqlalchemy_utils import aggregated
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import HSTORE
from app.general.utils.DatabaseLocalization import translation_hybrid
from app.integrations.models import Integration
from pydantic_choices import choice

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

    difficulty = Column(String)
    targets = Column(ARRAY(String), default=list)
    licence = Column(String)
    types = Column(ARRAY(String), default=list)
    # related_interlinkers
    administrative_scopes = Column(ARRAY(String), default=list)
    # domain = Column(String, nullable=True)
    process = Column(String, nullable=True)
    constraints_and_limitations = Column(String, nullable=True)
    regulations_and_standards = Column(String, nullable=True)

    constraints_and_limitations_translations = Column(HSTORE)
    regulations_and_standards_translations = Column(HSTORE, nullable=True)

    constraints_and_limitations = translation_hybrid(constraints_and_limitations_translations)
    regulations_and_standards = translation_hybrid(regulations_and_standards_translations)
    # discriminator
    nature = Column(String)
    
    __mapper_args__ = {
        "polymorphic_identity": "interlinker",
        "polymorphic_on": nature,
    }

    def __repr__(self) -> str:
        return f"<Interlinker {self.name}>"

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
        return f"<SoftwareInterlinker {self.name}>"

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

    representations = relationship(
        "Representation",
        back_populates="knowledgeinterlinker",
    )
    @aggregated('representations', Column(Integer))
    def representations_count(self):
        return func.count('1')

    __mapper_args__ = {
        "polymorphic_identity": "knowledgeinterlinker",
    }

    def __repr__(self) -> str:
        return f"<KnowledgeInterlinker {self.name}>"

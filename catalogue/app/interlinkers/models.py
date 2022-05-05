import enum
import uuid

from pydantic_choices import choice
from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    Enum,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import HSTORE, UUID
from sqlalchemy.orm import backref, relationship

from app.artefacts.models import Artefact
from app.config import settings
from app.locales import translation_hybrid


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

    published = Column(Boolean, default=False)
    logotype = Column(String, nullable=True)
    snapshots = Column(ARRAY(String), default=list)

    difficulty = Column(String)
    targets = Column(ARRAY(String), default=list)
    types = Column(ARRAY(String), default=list)
    administrative_scopes = Column(ARRAY(String), default=list)
    # domain = Column(String, nullable=True)
    process = Column(String, nullable=True)

    # discriminator
    nature = Column(String)
    
    instructions_translations = Column(HSTORE)
    instructions = translation_hybrid(instructions_translations)

    form = Column(String, nullable=True)
    format = Column(String, nullable=True)

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
    service_name = Column(String)
    domain = Column(String)
    path = Column(String)
    is_subdomain = Column(Boolean, default=False)
    api_path = Column(String)
    auth_method = Column(String)

    # capabilities
    instantiate = Column(Boolean, default=False)
    view = Column(Boolean, default=False)
    edit = Column(Boolean, default=False)
    clone = Column(Boolean, default=False)
    delete = Column(Boolean, default=False)
    download = Column(Boolean, default=False)
    preview = Column(Boolean, default=False)
    open_in_modal = Column(Boolean, default=False)
    shortcut = Column(Boolean, default=False)
    supports_internationalization = Column(Boolean, default=False)
    is_responsive = Column(Boolean, default=False)
    
    # capabilities translations
    instantiate_text_translations = Column(HSTORE)
    view_text_translations = Column(HSTORE)
    edit_text_translations = Column(HSTORE)
    delete_text_translations = Column(HSTORE)
    clone_text_translations = Column(HSTORE)
    download_text_translations = Column(HSTORE)
    preview_text_translations = Column(HSTORE)

    instantiate_text = translation_hybrid(instantiate_text_translations)
    view_text = translation_hybrid(view_text_translations)
    clone_text = translation_hybrid(clone_text_translations)
    edit_text = translation_hybrid(edit_text_translations)
    delete_text = translation_hybrid(delete_text_translations)
    download_text = translation_hybrid(download_text_translations)
    preview_text = translation_hybrid(preview_text_translations)
    
    status = Column(String, default="off")
    __mapper_args__ = {
        "polymorphic_identity": "softwareinterlinker",
    }

    def __repr__(self) -> str:
        return f"<SoftwareInterlinker {self.id}>"

    @property
    def backend(self):
        SERVER_NAME = self.domain or settings.SERVER_NAME
        if self.is_subdomain:
            return f"{settings.PROTOCOL}{self.path}.{SERVER_NAME}{self.api_path}"
        return f"{settings.PROTOCOL}{SERVER_NAME}/{self.path}{self.api_path}"

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
        backend = self.softwareinterlinker.service_name
        api_path = self.softwareinterlinker.api_path
        return f"http://{backend}{api_path}/{self.genesis_asset_id}"


class ExternalKnowledgeInterlinker(Interlinker):
    """
    Defines the external interlinker model
    """
    id = Column(
        UUID(as_uuid=True),
        ForeignKey("interlinker.id"),
        primary_key=True,
        default=uuid.uuid4,
    )
    uri_translations = Column(HSTORE)
    uri = translation_hybrid(uri_translations)
    asset_name_translations = Column(HSTORE)
    asset_name = translation_hybrid(asset_name_translations)

    __mapper_args__ = {
        "polymorphic_identity": "externalknowledgeinterlinker",
    }

    def __repr__(self) -> str:
        return f"<ExternalInterlinker {self.id}>"


class ExternalSoftwareInterlinker(Interlinker):
    """
    Defines the external interlinker model
    """
    id = Column(
        UUID(as_uuid=True),
        ForeignKey("interlinker.id"),
        primary_key=True,
        default=uuid.uuid4,
    )
    uri_translations = Column(HSTORE)
    uri = translation_hybrid(uri_translations)
    asset_name_translations = Column(HSTORE)
    asset_name = translation_hybrid(asset_name_translations)

    __mapper_args__ = {
        "polymorphic_identity": "externalsoftwareinterlinker",
    }

    def __repr__(self) -> str:
        return f"<ExternalInterlinker {self.id}>"
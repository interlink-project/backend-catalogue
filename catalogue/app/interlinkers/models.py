import uuid

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
from sqlalchemy.orm import relationship

from app.artefacts.models import Artefact
from app.general.db.base_class import Base as BaseModel
from werkzeug.utils import cached_property

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

    is_implementation_type = Column(Boolean, default=False)
    is_coproduction_type = Column(Boolean, default=False)
    SOC_type = Column(String)
    administrative_scope = Column(String, nullable=True)
    specific_app_domain = Column(ARRAY(String), nullable=True)
    constraints = Column(ARRAY(String), nullable=True)
    regulations = Column(ARRAY(String), nullable=True)

    nature = Column(String)
    # SW or KN
    software_type = Column(String, nullable=True)
    # IM or SP
    software_implementation = Column(String, nullable=True)
    # OS, OP, SAAS
    software_customization = Column(String, nullable=True)
    software_integration = Column(String, nullable=True)
    knowledge_type = Column(String, nullable=True)
    # IM or SP
    knowledge_format = Column(String, nullable=True)
    use_drive = Column(Boolean, default=True)
    
    # version
    backend = Column(String)
    # If knowledge interlinker, needs to have init template
    init_asset_id = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "interlinker",
    }

    def __repr__(self) -> str:
        return f"<Interlinker {self.name}>"

    @cached_property
    def is_knowledge(self):
        return self.nature == "KN"
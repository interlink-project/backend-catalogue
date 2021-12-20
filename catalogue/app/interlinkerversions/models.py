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

from app.general.db.base_class import Base as BaseModel

class InterlinkerVersion(BaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String)
    
    documentation = Column(String)
    interlinker_id = Column(
        UUID(as_uuid=True), ForeignKey("interlinker.id")
    )
    interlinker = relationship("Interlinker", back_populates="versions")
    
    backend = Column(String)
    # If knowledge interlinker, needs to have init template
    init_asset_id = Column(String, nullable=True)

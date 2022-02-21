import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.general.db.base_class import Base as BaseModel


class Representation(BaseModel):
    """
    Defines the representations model
    """
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    language = Column(String)
    form = Column(String)
    format = Column(String)
    knowledgeinterlinker_id = Column(UUID(as_uuid=True), ForeignKey("knowledgeinterlinker.id", ondelete='CASCADE'))
    knowledgeinterlinker = relationship("KnowledgeInterlinker", back_populates='representations')

    softwareinterlinker_id = Column(UUID(as_uuid=True), ForeignKey("softwareinterlinker.id", ondelete='SET NULL'))
    softwareinterlinker = relationship("SoftwareInterlinker", backref='representations')
    genesis_asset_id = Column(String)

    @property
    def link(self):
        return f"{self.softwareinterlinker.backend}/{self.genesis_asset_id}"

    def __repr__(self) -> str:
        return f"<Representation for {self.knowledgeinterlinker.name}>"

import uuid
from datetime import datetime

from app.general.db.base_class import Base as BaseModel
from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship


class QuestionComment(BaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String)

    artefact_id = Column(UUID(as_uuid=True), ForeignKey("artefact.id"))
    artefact = relationship("Artefact", back_populates="questioncomments")

    title = Column(String, nullable=True)
    text = Column(Text)
    
    parent_id = Column(UUID(as_uuid=True), ForeignKey("questioncomment.id"))
    children = relationship(
        "QuestionComment", backref=backref("parent", remote_side=[id])
    )

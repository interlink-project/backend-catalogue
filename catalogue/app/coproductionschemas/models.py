import uuid
from sqlalchemy import (
    Boolean,
    Column,
    String,
    ForeignKey,
    Table
)
from sqlalchemy.dialects.postgresql import HSTORE, UUID, ARRAY
from sqlalchemy.orm import relationship

from app.general.db.base_class import Base as BaseModel
from app.locales import translation_hybrid
from sqlalchemy.ext.associationproxy import association_proxy
from app.artefacts.models import Artefact

phases_prerequisites_metadata = Table(
    'phases_metadata_prerequisites', BaseModel.metadata,
    Column('phasemetadata_a_id', ForeignKey('phasemetadata.id'), primary_key=True),
    Column('phasemetadata_b_id', ForeignKey('phasemetadata.id', ondelete="CASCADE"), primary_key=True)
)


objectives_prerequisites_metadata = Table(
    'objective_metadata_prerequisites', BaseModel.metadata,
    Column('objectivemetadata_a_id', ForeignKey('objectivemetadata.id'), primary_key=True),
    Column('objectivemetadata_b_id', ForeignKey('objectivemetadata.id', ondelete="CASCADE"), primary_key=True)
)


tasks_prerequisites_metadata = Table(
    'tasks_metadata_prerequisites', BaseModel.metadata,
    Column('taskmetadata_a_id', ForeignKey('taskmetadata.id'), primary_key=True),
    Column('taskmetadata_b_id', ForeignKey('taskmetadata.id', ondelete="CASCADE"), primary_key=True)
)

tasks_problemprofiles_association = Table(
    'tasks_problemprofiles_association', BaseModel.metadata,
    Column('taskmetadata_a_id', ForeignKey('taskmetadata.id'), primary_key=True),
    Column('problemprofile_id', ForeignKey('problemprofile.id', ondelete="CASCADE"), primary_key=True)
)


class CoproductionSchema(Artefact):
    """
    Defines phase structure of a coproduction process.
    Inherits from artefact (name, description, tags...)
    """
    id = Column(
        UUID(as_uuid=True),
        ForeignKey("artefact.id"),
        primary_key=True,
        default=uuid.uuid4,
    )

    phasemetadatas = relationship("PhaseMetadata", back_populates="coproductionschema")

    __mapper_args__ = {
        "polymorphic_identity": "coproductionschema",
    }

    def __repr__(self):
        return "<CoproductionSchema %r>" % self.name



class PhaseMetadata(BaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_translations = Column(HSTORE)
    description_translations = Column(HSTORE)

    name = translation_hybrid(name_translations)
    description = translation_hybrid(description_translations)

    # prerequisites
    prerequisites = relationship("PhaseMetadata", secondary=phases_prerequisites_metadata,
                                 primaryjoin=id == phases_prerequisites_metadata.c.phasemetadata_a_id,
                                 secondaryjoin=id == phases_prerequisites_metadata.c.phasemetadata_b_id,
                                 )
    prerequisites_ids = association_proxy('prerequisites', 'id')

    # or can belong to an schema
    coproductionschema_id = Column(
        UUID(as_uuid=True), ForeignKey("coproductionschema.id", ondelete='CASCADE')
    )
    coproductionschema = relationship(
        "CoproductionSchema", back_populates="phasemetadatas")

    objectivemetadatas = relationship(
        "ObjectiveMetadata", back_populates="phasemetadata")

    def __repr__(self):
        return "<PhaseMetadata %r>" % self.name_translations["en"]

class ObjectiveMetadata(BaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_translations = Column(HSTORE)
    description_translations = Column(HSTORE)

    name = translation_hybrid(name_translations)
    description = translation_hybrid(description_translations)

    # belongs to a phasemetadata
    phasemetadata_id = Column(
        UUID(as_uuid=True), ForeignKey("phasemetadata.id", ondelete='CASCADE')
    )
    phasemetadata = relationship("PhaseMetadata", back_populates="objectivemetadatas")

    # prerequisites
    prerequisites = relationship("ObjectiveMetadata", secondary=objectives_prerequisites_metadata,
                                 primaryjoin=id == objectives_prerequisites_metadata.c.objectivemetadata_a_id,
                                 secondaryjoin=id == objectives_prerequisites_metadata.c.objectivemetadata_b_id,
                                 )
    prerequisites_ids = association_proxy('prerequisites', 'id')

    taskmetadatas = relationship("TaskMetadata", back_populates="objectivemetadata")

    def __repr__(self):
        return "<ObjectiveMetadata %r>" % self.name_translations["en"]


class TaskMetadata(BaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_translations = Column(HSTORE)
    description_translations = Column(HSTORE)

    name = translation_hybrid(name_translations)
    description = translation_hybrid(description_translations)

    # belongs to an objetive
    objectivemetadata_id = Column(
        UUID(as_uuid=True), ForeignKey("objectivemetadata.id", ondelete='CASCADE')
    )
    objectivemetadata = relationship("ObjectiveMetadata", back_populates="taskmetadatas")

    problemprofiles = relationship(
        "ProblemProfile",
        secondary=tasks_problemprofiles_association,
        backref="taskmetadatas")
    problemprofiles_ids = association_proxy('problemprofiles', 'id')
    
    # prerequisites
    prerequisites = relationship("TaskMetadata", secondary=tasks_prerequisites_metadata,
                                 primaryjoin=id == tasks_prerequisites_metadata.c.taskmetadata_a_id,
                                 secondaryjoin=id == tasks_prerequisites_metadata.c.taskmetadata_b_id,
    )
    prerequisites_ids = association_proxy('prerequisites', 'id')

    def __repr__(self):
        return "<TaskMetadata %r>" % self.name_translations["en"]

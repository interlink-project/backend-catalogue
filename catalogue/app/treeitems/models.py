
import enum
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    func,
    orm,
)
from sqlalchemy.dialects.postgresql import HSTORE, UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref

from app.general.db.base_class import Base as BaseModel
from app.locales import translation_hybrid

class TreeItemTypes(str, enum.Enum):
    task = "task"
    objective = "objective"
    phase = "phase"

prerequisites = Table(
    'treeitemmetadata_prerequisites', BaseModel.metadata,
    Column('treeitemmetadata_a_id', ForeignKey(
        'treeitemmetadata.id', ondelete="CASCADE"), primary_key=True),
    Column('treeitemmetadata_b_id', ForeignKey(
        'treeitemmetadata.id', ondelete="CASCADE"), primary_key=True)
)
treeitems_problemprofiles_association = Table(
    'treeitemmetadata_problemprofiles_association', BaseModel.metadata,
    Column('treeitemmetadata_a_id', ForeignKey('treeitemmetadata.id', ondelete="CASCADE"), primary_key=True),
    Column('problemprofile_id', ForeignKey('problemprofile.id', ondelete="CASCADE"), primary_key=True)
)

class TreeItemMetadata(BaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_translations = Column(HSTORE)
    description_translations = Column(HSTORE)

    name = translation_hybrid(name_translations)
    description = translation_hybrid(description_translations)

    type = Column(Enum(TreeItemTypes, create_constraint=False,native_enum=False), default=TreeItemTypes.task)

    # children
    parent_id = Column(UUID(as_uuid=True), ForeignKey("treeitemmetadata.id", ondelete='CASCADE'))
    children = orm.relationship(
        "TreeItemMetadata", backref=orm.backref("parent", remote_side=[id])
    )
    children_ids = association_proxy('children', 'id')

    # or can belong to an schema
    coproductionschema_id = Column(
        UUID(as_uuid=True), ForeignKey("coproductionschema.id", ondelete='CASCADE')
    )
    coproductionschema = relationship(
        "CoproductionSchema", backref=backref('children', passive_deletes=True))

    # prerequisites
    prerequisites = orm.relationship("TreeItemMetadata", secondary=prerequisites,
                                     primaryjoin=id == prerequisites.c.treeitemmetadata_a_id,
                                     secondaryjoin=id == prerequisites.c.treeitemmetadata_b_id,
                                     )

    prerequisites_ids = association_proxy('prerequisites', 'id')

    problemprofiles = relationship(
        "ProblemProfile",
        secondary=treeitems_problemprofiles_association,
        backref="treeitemmetadatas")
    problemprofiles_ids = association_proxy('problemprofiles', 'id')

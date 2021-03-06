"""treeitems

Revision ID: 27c8315a7dd8
Revises: 
Create Date: 2022-06-28 16:46:42.969327

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '27c8315a7dd8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artefact',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('artefact_type', sa.String(length=70), nullable=True),
    sa.Column('languages', sa.ARRAY(sa.String()), server_default='{}', nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=True),
    sa.Column('licence', sa.String(), nullable=True),
    sa.Column('name_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('description_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('constraints_and_limitations_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('regulations_and_standards_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('tags_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('rating', sa.Numeric(precision=2, scale=1), nullable=True),
    sa.Column('ratings_count', sa.Integer(), nullable=True),
    sa.Column('creator_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('problemprofile',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('description_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('functionality_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('artefact_problem',
    sa.Column('artefact_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('problemprofile_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['artefact_id'], ['artefact.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['problemprofile_id'], ['problemprofile.id'], ondelete='CASCADE')
    )
    op.create_table('coproductionschema',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['artefact.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('interlinker',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_sustainability_related', sa.Boolean(), nullable=True),
    sa.Column('published', sa.Boolean(), nullable=True),
    sa.Column('logotype', sa.String(), nullable=True),
    sa.Column('snapshots', sa.ARRAY(sa.String()), server_default='{}', nullable=True),
    sa.Column('difficulty', sa.String(), nullable=True),
    sa.Column('targets', sa.ARRAY(sa.String()), server_default='{}', nullable=True),
    sa.Column('types', sa.ARRAY(sa.String()), server_default='{}', nullable=True),
    sa.Column('administrative_scopes', sa.ARRAY(sa.String()), server_default='{}', nullable=True),
    sa.Column('process', sa.String(), nullable=True),
    sa.Column('nature', sa.String(), nullable=True),
    sa.Column('instructions_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('form', sa.String(), nullable=True),
    sa.Column('format', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['artefact.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publicservice',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('language', sa.String(), nullable=True),
    sa.Column('processing_time', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('public_organization', sa.String(), nullable=True),
    sa.Column('output', sa.String(), nullable=True),
    sa.Column('cost', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['artefact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rating',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('artefact_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['artefact_id'], ['artefact.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('externalknowledgeinterlinker',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('uri_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('asset_name_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['interlinker.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('externalsoftwareinterlinker',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('uri_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('asset_name_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['interlinker.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('softwareinterlinker',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('supported_by', sa.ARRAY(sa.Enum('saas', 'on_premise', 'installed_app', name='supporters', native_enum=False)), nullable=True),
    sa.Column('service_name', sa.String(), nullable=True),
    sa.Column('domain', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('is_subdomain', sa.Boolean(), nullable=True),
    sa.Column('api_path', sa.String(), nullable=True),
    sa.Column('auth_method', sa.String(), nullable=True),
    sa.Column('instantiate', sa.Boolean(), nullable=True),
    sa.Column('view', sa.Boolean(), nullable=True),
    sa.Column('edit', sa.Boolean(), nullable=True),
    sa.Column('clone', sa.Boolean(), nullable=True),
    sa.Column('delete', sa.Boolean(), nullable=True),
    sa.Column('download', sa.Boolean(), nullable=True),
    sa.Column('preview', sa.Boolean(), nullable=True),
    sa.Column('open_in_modal', sa.Boolean(), nullable=True),
    sa.Column('shortcut', sa.Boolean(), nullable=True),
    sa.Column('supports_internationalization', sa.Boolean(), nullable=True),
    sa.Column('is_responsive', sa.Boolean(), nullable=True),
    sa.Column('instantiate_text_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('view_text_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('edit_text_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('delete_text_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('clone_text_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('download_text_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('preview_text_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['interlinker.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('treeitemmetadata',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('description_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('type', sa.Enum('task', 'objective', 'phase', name='treeitemtypes', native_enum=False), nullable=True),
    sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('coproductionschema_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('is_part_of_codelivery', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['coproductionschema_id'], ['coproductionschema.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['parent_id'], ['treeitemmetadata.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('knowledgeinterlinker',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('softwareinterlinker_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('genesis_asset_id_translations', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['interlinker.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['parent_id'], ['knowledgeinterlinker.id'], ),
    sa.ForeignKeyConstraint(['softwareinterlinker_id'], ['softwareinterlinker.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('treeitemmetadata_prerequisites',
    sa.Column('treeitemmetadata_a_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('treeitemmetadata_b_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['treeitemmetadata_a_id'], ['treeitemmetadata.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['treeitemmetadata_b_id'], ['treeitemmetadata.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('treeitemmetadata_a_id', 'treeitemmetadata_b_id')
    )
    op.create_table('treeitemmetadata_problemprofiles_association',
    sa.Column('treeitemmetadata_a_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('problemprofile_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['problemprofile_id'], ['problemprofile.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['treeitemmetadata_a_id'], ['treeitemmetadata.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('treeitemmetadata_a_id', 'problemprofile_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('treeitemmetadata_problemprofiles_association')
    op.drop_table('treeitemmetadata_prerequisites')
    op.drop_table('knowledgeinterlinker')
    op.drop_table('treeitemmetadata')
    op.drop_table('softwareinterlinker')
    op.drop_table('externalsoftwareinterlinker')
    op.drop_table('externalknowledgeinterlinker')
    op.drop_table('rating')
    op.drop_table('publicservice')
    op.drop_table('interlinker')
    op.drop_table('coproductionschema')
    op.drop_table('artefact_problem')
    op.drop_table('problemprofile')
    op.drop_table('artefact')
    # ### end Alembic commands ###

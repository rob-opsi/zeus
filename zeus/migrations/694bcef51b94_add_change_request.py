"""add_change_request

Revision ID: 694bcef51b94
Revises: f78a2be4ddf9
Create Date: 2018-01-15 13:53:12.680830

"""
from alembic import op
import sqlalchemy as sa
import zeus


# revision identifiers, used by Alembic.
revision = '694bcef51b94'
down_revision = 'f78a2be4ddf9'
branch_labels = ()
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('change_request',
                    sa.Column('number', sa.Integer(), nullable=False),
                    sa.Column('parent_revision_sha', sa.String(length=40), nullable=False),
                    sa.Column('head_revision_sha', sa.String(length=40), nullable=True),
                    sa.Column('message', sa.String(), nullable=False),
                    sa.Column('author_id', zeus.db.types.guid.GUID(), nullable=True),
                    sa.Column('provider', sa.String(), nullable=True),
                    sa.Column('external_id', sa.String(length=64), nullable=True),
                    sa.Column('url', sa.String(), nullable=True),
                    sa.Column('data', zeus.db.types.json.JSONEncodedDict(), nullable=True),
                    sa.Column('date_updated', sa.TIMESTAMP(timezone=True), nullable=True),
                    sa.Column('repository_id', zeus.db.types.guid.GUID(), nullable=False),
                    sa.Column('id', zeus.db.types.guid.GUID(), nullable=False),
                    sa.Column(
                        'date_created',
                        sa.TIMESTAMP(
                            timezone=True),
                        server_default=sa.text('now()'),
                        nullable=False),
                    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
                    sa.ForeignKeyConstraint(['repository_id', 'head_revision_sha'], [
                        'revision.repository_id', 'revision.sha'], ),
                    sa.ForeignKeyConstraint(['repository_id', 'parent_revision_sha'], [
                        'revision.repository_id', 'revision.sha'], ),
                    sa.ForeignKeyConstraint(
                        ['repository_id'], ['repository.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('repository_id', 'number', name='unq_cr_number'),
                    sa.UniqueConstraint(
                        'repository_id',
                        'provider',
                        'external_id',
                        name='unq_cr_provider')
                    )
    op.create_index('idx_cr_head_revision', 'change_request', [
                    'repository_id', 'head_revision_sha'], unique=False)
    op.create_index('idx_cr_parent_revision', 'change_request', [
                    'repository_id', 'parent_revision_sha'], unique=False)
    op.create_index(
        op.f('ix_change_request_author_id'),
        'change_request',
        ['author_id'],
        unique=False)
    op.create_index(
        op.f('ix_change_request_repository_id'),
        'change_request',
        ['repository_id'],
        unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_change_request_repository_id'), table_name='change_request')
    op.drop_index(op.f('ix_change_request_author_id'), table_name='change_request')
    op.drop_index('idx_cr_parent_revision', table_name='change_request')
    op.drop_index('idx_cr_head_revision', table_name='change_request')
    op.drop_table('change_request')
    # ### end Alembic commands ###
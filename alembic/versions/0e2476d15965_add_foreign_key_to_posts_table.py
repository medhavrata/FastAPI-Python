"""add foreign key to posts table

Revision ID: 0e2476d15965
Revises: 17660fbb01a0
Create Date: 2021-11-16 18:45:10.799604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e2476d15965'
down_revision = '17660fbb01a0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraing('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass

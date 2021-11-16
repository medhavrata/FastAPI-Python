"""creating posts table

Revision ID: a367f1fcdb8a
Revises: 
Create Date: 2021-11-16 17:02:56.113905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a367f1fcdb8a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')

"""adding column in posts table

Revision ID: d4141d855ad2
Revises: a367f1fcdb8a
Create Date: 2021-11-16 18:30:21.829038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4141d855ad2'
down_revision = 'a367f1fcdb8a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

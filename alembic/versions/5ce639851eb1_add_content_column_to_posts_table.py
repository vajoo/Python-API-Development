"""add content column to posts table

Revision ID: 5ce639851eb1
Revises: 7ac7ba9d5c41
Create Date: 2023-05-27 12:46:24.123870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ce639851eb1'
down_revision = '7ac7ba9d5c41'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
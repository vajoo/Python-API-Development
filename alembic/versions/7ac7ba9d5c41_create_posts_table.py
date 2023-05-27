"""create posts table

Revision ID: 7ac7ba9d5c41
Revises: 
Create Date: 2023-05-27 12:23:42.753108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ac7ba9d5c41'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('posts')
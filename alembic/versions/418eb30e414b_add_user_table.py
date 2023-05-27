"""add user table

Revision ID: 418eb30e414b
Revises: 5ce639851eb1
Create Date: 2023-05-27 13:04:01.381385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '418eb30e414b'
down_revision = '5ce639851eb1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table('users')

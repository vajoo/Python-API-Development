"""autogenerate votes table

Revision ID: 838b9f3605fe
Revises: 4e7229814c90
Create Date: 2023-05-27 15:13:01.868202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '838b9f3605fe'
down_revision = '4e7229814c90'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    )


def downgrade() -> None:
    op.drop_table('votes')
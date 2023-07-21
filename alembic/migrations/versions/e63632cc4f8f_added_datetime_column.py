"""added datetime column

Revision ID: e63632cc4f8f
Revises: 002f15c78416
Create Date: 2023-07-20 17:25:24.886795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e63632cc4f8f'
down_revision = '002f15c78416'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('created_at', sa.TIMESTAMP(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notes', 'created_at')
    # ### end Alembic commands ###
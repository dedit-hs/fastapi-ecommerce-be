"""New Migrations

Revision ID: 5d353c8c4bce
Revises: b9dab0b8921b
Create Date: 2023-05-15 23:18:36.321320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d353c8c4bce'
down_revision = 'b9dab0b8921b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('size', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cart', 'size')
    # ### end Alembic commands ###
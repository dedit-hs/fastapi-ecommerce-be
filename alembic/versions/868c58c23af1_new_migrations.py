"""new migrations

Revision ID: 868c58c23af1
Revises: c1a5f211603d
Create Date: 2023-05-12 14:24:43.386808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '868c58c23af1'
down_revision = 'c1a5f211603d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'customer', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'customer', type_='unique')
    # ### end Alembic commands ###

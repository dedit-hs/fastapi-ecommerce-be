"""update table

Revision ID: 59bf4278f103
Revises: a26a5c1d81b1
Create Date: 2023-05-14 10:42:09.660110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59bf4278f103'
down_revision = 'a26a5c1d81b1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('product_size_size_id_fkey', 'product_size', type_='foreignkey')
    op.create_foreign_key(None, 'product_size', 'size', ['size_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product_size', type_='foreignkey')
    op.create_foreign_key('product_size_size_id_fkey', 'product_size', 'image', ['size_id'], ['id'])
    # ### end Alembic commands ###
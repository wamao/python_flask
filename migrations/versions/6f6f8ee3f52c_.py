"""empty message

Revision ID: 6f6f8ee3f52c
Revises: 0963a4bc648e
Create Date: 2018-06-05 16:17:21.315000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f6f8ee3f52c'
down_revision = '0963a4bc648e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('cartId', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cart', 'cartId')
    # ### end Alembic commands ###

"""empty message

Revision ID: 4467254a96f1
Revises: 
Create Date: 2018-06-01 09:24:46.565000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4467254a96f1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ContactPerson', sa.String(length=255), nullable=False),
    sa.Column('ContactNumber', sa.String(length=255), nullable=False),
    sa.Column('ContactAddress', sa.String(length=255), nullable=False),
    sa.Column('ContactDetailAddress', sa.String(length=255), nullable=False),
    sa.Column('AddressId', sa.String(length=255), nullable=False),
    sa.Column('isDefault', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column(u'user', 'password',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column(u'user', 'username',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(u'user', 'username',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column(u'user', 'password',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.drop_table('address')
    # ### end Alembic commands ###

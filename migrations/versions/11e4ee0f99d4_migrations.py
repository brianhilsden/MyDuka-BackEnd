"""migrations

Revision ID: 11e4ee0f99d4
Revises: e511f4dd376c
Create Date: 2024-08-12 00:37:46.029005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11e4ee0f99d4'
down_revision = 'e511f4dd376c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_number', sa.String(), nullable=True))

    with op.batch_alter_table('clerks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_number', sa.String(), nullable=True))

    with op.batch_alter_table('merchants', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_number', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('merchants', schema=None) as batch_op:
        batch_op.drop_column('phone_number')

    with op.batch_alter_table('clerks', schema=None) as batch_op:
        batch_op.drop_column('phone_number')

    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.drop_column('phone_number')

    # ### end Alembic commands ###

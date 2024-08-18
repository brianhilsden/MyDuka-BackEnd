"""updates

Revision ID: da55902b7690
Revises: 11e4ee0f99d4
Create Date: 2024-08-16 14:23:12.571373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da55902b7690'
down_revision = '11e4ee0f99d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('brand_name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('brand_name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###

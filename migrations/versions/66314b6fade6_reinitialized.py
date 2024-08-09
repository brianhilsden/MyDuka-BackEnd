"""reinitialized

Revision ID: 66314b6fade6
Revises: 00210b70e1e1
Create Date: 2024-08-09 14:41:40.125115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66314b6fade6'
down_revision = '00210b70e1e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('_password_hash', sa.String(), nullable=True),
    sa.Column('account_status', sa.String(), nullable=True),
    sa.Column('store_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clerks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('_password_hash', sa.String(), nullable=True),
    sa.Column('account_status', sa.String(), nullable=True),
    sa.Column('store_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('merchants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('_password_hash', sa.String(), nullable=True),
    sa.Column('store_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brand_name', sa.String(), nullable=False),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('availability', sa.Boolean(), nullable=True),
    sa.Column('payment_status', sa.String(), nullable=False),
    sa.Column('received_items', sa.Integer(), nullable=True),
    sa.Column('closing_stock', sa.Integer(), nullable=False),
    sa.Column('spoilt_items', sa.Integer(), nullable=True),
    sa.Column('buying_price', sa.Float(), nullable=False),
    sa.Column('selling_price', sa.Float(), nullable=False),
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('clerk_id', sa.Integer(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('store_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admins.id'], ),
    sa.ForeignKeyConstraint(['clerk_id'], ['clerks.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('salesReports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('product_name', sa.String(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('store_id', sa.Integer(), nullable=True),
    sa.Column('clerk_id', sa.Integer(), nullable=True),
    sa.Column('quantity_sold', sa.Integer(), nullable=True),
    sa.Column('quantity_in_hand', sa.Integer(), nullable=True),
    sa.Column('profit', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['clerk_id'], ['clerks.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('salesReports')
    op.drop_table('requests')
    op.drop_table('products')
    op.drop_table('merchants')
    op.drop_table('clerks')
    op.drop_table('admins')
    op.drop_table('stores')
    # ### end Alembic commands ###

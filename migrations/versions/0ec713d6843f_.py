"""empty message

Revision ID: 0ec713d6843f
Revises: 
Create Date: 2017-10-31 16:18:01.999512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ec713d6843f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('item', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contractors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_id', sa.String(length=64), nullable=True),
    sa.Column('name_first', sa.String(length=64), nullable=True),
    sa.Column('name_last', sa.String(length=64), nullable=True),
    sa.Column('street_number', sa.String(length=64), nullable=True),
    sa.Column('street_name', sa.String(length=64), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('state', sa.String(length=64), nullable=True),
    sa.Column('country', sa.String(length=64), nullable=True),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_id', sa.String(length=64), nullable=True),
    sa.Column('data', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inspections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_id', sa.String(length=64), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('item', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('learning',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_id', sa.String(length=64), nullable=True),
    sa.Column('data', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_id', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('street_number', sa.String(length=64), nullable=True),
    sa.Column('street_name', sa.String(length=64), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('state', sa.String(length=64), nullable=True),
    sa.Column('country', sa.String(length=64), nullable=True),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_id', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('item', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assigned',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_id', sa.String(length=64), nullable=True),
    sa.Column('contractor', sa.String(length=64), nullable=True),
    sa.Column('inspection', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['contractor'], ['contractors.id'], ),
    sa.ForeignKeyConstraint(['inspection'], ['inspections.id'], ),
    sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assigned')
    op.drop_table('users')
    op.drop_table('sites')
    op.drop_table('learning')
    op.drop_table('inspections')
    op.drop_table('data')
    op.drop_table('contractors')
    op.drop_table('organizations')
    # ### end Alembic commands ###
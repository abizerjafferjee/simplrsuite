"""empty message

Revision ID: 9bf419b32cbd
Revises: 0392c6140080
Create Date: 2019-10-04 06:14:47.132099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bf419b32cbd'
down_revision = '0392c6140080'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('business_name', sa.String(), nullable=True),
    sa.Column('contact_person', sa.String(), nullable=True),
    sa.Column('email_one', sa.String(), nullable=True),
    sa.Column('email_two', sa.String(), nullable=True),
    sa.Column('phone_one', sa.String(), nullable=True),
    sa.Column('phone_two', sa.String(), nullable=True),
    sa.Column('plus_code', sa.String(), nullable=True),
    sa.Column('additional_info', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('supplier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('business_name', sa.String(), nullable=True),
    sa.Column('contact_person', sa.String(), nullable=True),
    sa.Column('email_one', sa.String(), nullable=True),
    sa.Column('email_two', sa.String(), nullable=True),
    sa.Column('phone_one', sa.String(), nullable=True),
    sa.Column('phone_two', sa.String(), nullable=True),
    sa.Column('plus_code', sa.String(), nullable=True),
    sa.Column('additional_info', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('supplier')
    op.drop_table('customer')
    # ### end Alembic commands ###

"""empty message

Revision ID: 44d410976651
Revises: 04d02dd0aeb8
Create Date: 2019-09-24 06:21:47.529803

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '44d410976651'
down_revision = '04d02dd0aeb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('created', sa.DateTime(), nullable=True))
    op.drop_column('data', 'datetime')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('datetime', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('data', 'created')
    # ### end Alembic commands ###

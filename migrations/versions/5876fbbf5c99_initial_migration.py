"""Initial migration.

Revision ID: 5876fbbf5c99
Revises: 
Create Date: 2020-05-29 22:50:34.396622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5876fbbf5c99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'examples', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'examples', type_='unique')
    # ### end Alembic commands ###

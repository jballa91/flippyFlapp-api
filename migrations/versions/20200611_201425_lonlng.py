"""lonlng

Revision ID: 65949792aae8
Revises: 9ef4312d8dca
Create Date: 2020-06-11 20:14:25.273807

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '65949792aae8'
down_revision = '9ef4312d8dca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('airports', sa.Column('lng', sa.Float(), nullable=False))
    # op.drop_column('airports', 'lon')
    op.alter_column('airports', 'lon', nullable=False, new_column_name='lng')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('airports', sa.Column('lon', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    # op.drop_column('airports', 'lng')
    op.alter_column('airports', 'lng', nullable=False, new_column_name='lon')
    # ### end Alembic commands ###

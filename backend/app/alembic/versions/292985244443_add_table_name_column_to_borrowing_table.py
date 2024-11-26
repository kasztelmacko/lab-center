"""Add table_name column to borrowing table

Revision ID: 292985244443
Revises: 1a31ce608336
Create Date: 2024-11-26 12:04:01.378867

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '292985244443'
down_revision = 'e2412789c190'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('borrowing', sa.Column('table_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('borrowing', sa.Column('system_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('borrowing', 'system_name')
    op.drop_column('borrowing', 'table_name')
    # ### end Alembic commands ###

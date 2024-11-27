"""Add cascade delete relationships

Revision ID: 1a31ce608336
Revises: d98dd8ec85a3
Create Date: 2024-07-31 22:24:34.447891

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '1a31ce608336'
down_revision = 'd98dd8ec85a3'
branch_labels = None
depends_on = None


def upgrade():
    # Update Item table to use cascade delete for lab_id
    op.drop_constraint('item_lab_id_fkey', 'item', type_='foreignkey')
    op.create_foreign_key('item_lab_id_fkey', 'item', 'lab', ['lab_id'], ['lab_id'], ondelete='CASCADE')

    # Update Lab table to use cascade delete for owner_id
    op.drop_constraint('lab_owner_id_fkey', 'lab', type_='foreignkey')
    op.create_foreign_key('lab_owner_id_fkey', 'lab', 'user', ['owner_id'], ['user_id'], ondelete='CASCADE')

    # Update UserLab table to use cascade delete for user_id and lab_id
    op.drop_constraint('user_lab_user_id_fkey', 'user_lab', type_='foreignkey')
    op.create_foreign_key('user_lab_user_id_fkey', 'user_lab', 'user', ['user_id'], ['user_id'], ondelete='CASCADE')
    op.drop_constraint('user_lab_lab_id_fkey', 'user_lab', type_='foreignkey')
    op.create_foreign_key('user_lab_lab_id_fkey', 'user_lab', 'lab', ['lab_id'], ['lab_id'], ondelete='CASCADE')

    # Update Borrowing table to use cascade delete for user_id and item_id
    op.drop_constraint('borrowing_user_id_fkey', 'borrowing', type_='foreignkey')
    op.create_foreign_key('borrowing_user_id_fkey', 'borrowing', 'user', ['user_id'], ['user_id'], ondelete='CASCADE')
    op.drop_constraint('borrowing_item_id_fkey', 'borrowing', type_='foreignkey')
    op.create_foreign_key('borrowing_item_id_fkey', 'borrowing', 'item', ['item_id'], ['item_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # Revert Item table to remove cascade delete for lab_id
    op.drop_constraint('item_lab_id_fkey', 'item', type_='foreignkey')
    op.create_foreign_key('item_lab_id_fkey', 'item', 'lab', ['lab_id'], ['lab_id'])

    # Revert Lab table to remove cascade delete for owner_id
    op.drop_constraint('lab_owner_id_fkey', 'lab', type_='foreignkey')
    op.create_foreign_key('lab_owner_id_fkey', 'lab', 'user', ['owner_id'], ['user_id'])

    # Revert UserLab table to remove cascade delete for user_id and lab_id
    op.drop_constraint('user_lab_user_id_fkey', 'user_lab', type_='foreignkey')
    op.create_foreign_key('user_lab_user_id_fkey', 'user_lab', 'user', ['user_id'], ['user_id'])
    op.drop_constraint('user_lab_lab_id_fkey', 'user_lab', type_='foreignkey')
    op.create_foreign_key('user_lab_lab_id_fkey', 'user_lab', 'lab', ['lab_id'], ['lab_id'])

    # Revert Borrowing table to remove cascade delete for user_id and item_id
    op.drop_constraint('borrowing_user_id_fkey', 'borrowing', type_='foreignkey')
    op.create_foreign_key('borrowing_user_id_fkey', 'borrowing', 'user', ['user_id'], ['user_id'])
    op.drop_constraint('borrowing_item_id_fkey', 'borrowing', type_='foreignkey')
    op.create_foreign_key('borrowing_item_id_fkey', 'borrowing', 'item', ['item_id'], ['item_id'])
    # ### end Alembic commands ###

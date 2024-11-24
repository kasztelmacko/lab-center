"""Edit replace id integers in all models to use UUID instead

Revision ID: d98dd8ec85a3
Revises: 9c0a54914c78
Create Date: 2024-07-19 04:08:04.000976

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'd98dd8ec85a3'
down_revision = '9c0a54914c78'
branch_labels = None
depends_on = None


def upgrade():
    # Ensure uuid-ossp extension is available
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create new UUID columns with default UUID values
    op.add_column('user', sa.Column('new_user_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')))
    op.add_column('lab', sa.Column('new_lab_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')))
    op.add_column('item', sa.Column('new_item_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')))
    op.add_column('user_lab', sa.Column('new_userlab_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')))
    op.add_column('borrowing', sa.Column('new_borrow_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')))

    # Populate the new columns with UUIDs
    op.execute('UPDATE "user" SET new_user_id = uuid_generate_v4()')
    op.execute('UPDATE lab SET new_lab_id = uuid_generate_v4()')
    op.execute('UPDATE item SET new_item_id = uuid_generate_v4()')
    op.execute('UPDATE user_lab SET new_userlab_id = uuid_generate_v4()')
    op.execute('UPDATE borrowing SET new_borrow_id = uuid_generate_v4()')

    # Set the new columns as not nullable
    op.alter_column('user', 'new_user_id', nullable=False)
    op.alter_column('lab', 'new_lab_id', nullable=False)
    op.alter_column('item', 'new_item_id', nullable=False)
    op.alter_column('user_lab', 'new_userlab_id', nullable=False)
    op.alter_column('borrowing', 'new_borrow_id', nullable=False)

    # Drop old columns and rename new columns
    op.drop_column('user', 'user_id')
    op.alter_column('user', 'new_user_id', new_column_name='user_id')

    op.drop_column('lab', 'lab_id')
    op.alter_column('lab', 'new_lab_id', new_column_name='lab_id')

    op.drop_column('item', 'item_id')
    op.alter_column('item', 'new_item_id', new_column_name='item_id')

    op.drop_column('user_lab', 'userlab_id')
    op.alter_column('user_lab', 'new_userlab_id', new_column_name='userlab_id')

    op.drop_column('borrowing', 'borrow_id')
    op.alter_column('borrowing', 'new_borrow_id', new_column_name='borrow_id')

    # Recreate foreign key constraints
    op.drop_constraint('lab_owner_id_fkey', 'lab', type_='foreignkey')
    op.create_foreign_key('lab_owner_id_fkey', 'lab', 'user', ['owner_id'], ['user_id'], ondelete="CASCADE")

    op.drop_constraint('item_lab_id_fkey', 'item', type_='foreignkey')
    op.create_foreign_key('item_lab_id_fkey', 'item', 'lab', ['lab_id'], ['lab_id'], ondelete="CASCADE")

    op.drop_constraint('user_lab_user_id_fkey', 'user_lab', type_='foreignkey')
    op.create_foreign_key('user_lab_user_id_fkey', 'user_lab', 'user', ['user_id'], ['user_id'], ondelete="CASCADE")

    op.drop_constraint('borrowing_user_id_fkey', 'borrowing', type_='foreignkey')
    op.create_foreign_key('borrowing_user_id_fkey', 'borrowing', 'user', ['user_id'], ['user_id'], ondelete="CASCADE")

    op.drop_constraint('borrowing_item_id_fkey', 'borrowing', type_='foreignkey')
    op.create_foreign_key('borrowing_item_id_fkey', 'borrowing', 'item', ['item_id'], ['item_id'], ondelete="CASCADE")

def downgrade():
    # Reverse the upgrade process
    op.add_column('user', sa.Column('old_user_id', sa.Integer, autoincrement=True))
    op.add_column('lab', sa.Column('old_lab_id', sa.Integer, autoincrement=True))
    op.add_column('item', sa.Column('old_item_id', sa.Integer, autoincrement=True))
    op.add_column('user_lab', sa.Column('old_userlab_id', sa.Integer, autoincrement=True))
    op.add_column('borrowing', sa.Column('old_borrow_id', sa.Integer, autoincrement=True))

    # Populate the old columns with default values
    op.execute('UPDATE "user" SET old_user_id = nextval(\'user_id_seq\')')
    op.execute('UPDATE lab SET old_lab_id = nextval(\'lab_id_seq\')')
    op.execute('UPDATE item SET old_item_id = nextval(\'item_id_seq\')')
    op.execute('UPDATE user_lab SET old_userlab_id = nextval(\'user_lab_id_seq\')')
    op.execute('UPDATE borrowing SET old_borrow_id = nextval(\'borrowing_id_seq\')')

    # Drop new columns and rename old columns back
    op.drop_column('user', 'user_id')
    op.alter_column('user', 'old_user_id', new_column_name='user_id')

    op.drop_column('lab', 'lab_id')
    op.alter_column('lab', 'old_lab_id', new_column_name='lab_id')

    op.drop_column('item', 'item_id')
    op.alter_column('item', 'old_item_id', new_column_name='item_id')

    op.drop_column('user_lab', 'userlab_id')
    op.alter_column('user_lab', 'old_userlab_id', new_column_name='userlab_id')

    op.drop_column('borrowing', 'borrow_id')
    op.alter_column('borrowing', 'old_borrow_id', new_column_name='borrow_id')

    # Recreate foreign key constraints
    op.drop_constraint('lab_owner_id_fkey', 'lab', type_='foreignkey')
    op.create_foreign_key('lab_owner_id_fkey', 'lab', 'user', ['owner_id'], ['user_id'], ondelete="CASCADE")

    op.drop_constraint('item_lab_id_fkey', 'item', type_='foreignkey')
    op.create_foreign_key('item_lab_id_fkey', 'item', 'lab', ['lab_id'], ['lab_id'], ondelete="CASCADE")

    op.drop_constraint('user_lab_user_id_fkey', 'user_lab', type_='foreignkey')
    op.create_foreign_key('user_lab_user_id_fkey', 'user_lab', 'user', ['user_id'], ['user_id'], ondelete="CASCADE")

    op.drop_constraint('borrowing_user_id_fkey', 'borrowing', type_='foreignkey')
    op.create_foreign_key('borrowing_user_id_fkey', 'borrowing', 'user', ['user_id'], ['user_id'], ondelete="CASCADE")

    op.drop_constraint('borrowing_item_id_fkey', 'borrowing', type_='foreignkey')
    op.create_foreign_key('borrowing_item_id_fkey', 'borrowing', 'item', ['item_id'], ['item_id'], ondelete="CASCADE")
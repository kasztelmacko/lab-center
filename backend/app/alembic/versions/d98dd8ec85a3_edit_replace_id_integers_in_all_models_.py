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

    # Create a new UUID column with a default UUID value for User
    op.add_column('user', sa.Column('new_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')))
    op.execute('UPDATE "user" SET new_id = uuid_generate_v4()')
    op.alter_column('user', 'new_id', nullable=False)
    op.drop_column('user', 'id')
    op.alter_column('user', 'new_id', new_column_name='id')
    op.create_primary_key('user_pkey', 'user', ['id'])

    # Create a new UUID column with a default UUID value for Lab
    op.add_column('lab', sa.Column('new_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')))
    op.execute('UPDATE lab SET new_id = uuid_generate_v4()')
    op.alter_column('lab', 'new_id', nullable=False)
    op.drop_column('lab', 'id')
    op.alter_column('lab', 'new_id', new_column_name='id')
    op.create_primary_key('lab_pkey', 'lab', ['id'])

    # Update Lab's owner_id to use UUID
    op.add_column('lab', sa.Column('new_owner_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.execute('UPDATE lab SET new_owner_id = (SELECT new_id FROM "user" WHERE "user".id = lab.owner_id)')
    op.alter_column('lab', 'new_owner_id', nullable=False)
    op.drop_constraint('lab_owner_id_fkey', 'lab', type_='foreignkey')
    op.drop_column('lab', 'owner_id')
    op.alter_column('lab', 'new_owner_id', new_column_name='owner_id')
    op.create_foreign_key('lab_owner_id_fkey', 'lab', 'user', ['owner_id'], ['id'], ondelete='CASCADE')

    # Create a new UUID column with a default UUID value for Item
    op.add_column('item', sa.Column('new_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')))
    op.execute('UPDATE item SET new_id = uuid_generate_v4()')
    op.alter_column('item', 'new_id', nullable=False)
    op.drop_column('item', 'id')
    op.alter_column('item', 'new_id', new_column_name='id')
    op.create_primary_key('item_pkey', 'item', ['id'])

    # Update Item's lab_id to use UUID
    op.add_column('item', sa.Column('new_lab_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.execute('UPDATE item SET new_lab_id = (SELECT new_id FROM lab WHERE lab.id = item.lab_id)')
    op.alter_column('item', 'new_lab_id', nullable=False)
    op.drop_constraint('item_lab_id_fkey', 'item', type_='foreignkey')
    op.drop_column('item', 'lab_id')
    op.alter_column('item', 'new_lab_id', new_column_name='lab_id')
    op.create_foreign_key('item_lab_id_fkey', 'item', 'lab', ['lab_id'], ['id'], ondelete='CASCADE')

    # Create a new UUID column with a default UUID value for UserLab
    op.add_column('user_lab', sa.Column('new_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')))
    op.execute('UPDATE user_lab SET new_id = uuid_generate_v4()')
    op.alter_column('user_lab', 'new_id', nullable=False)
    op.drop_column('user_lab', 'id')
    op.alter_column('user_lab', 'new_id', new_column_name='id')
    op.create_primary_key('user_lab_pkey', 'user_lab', ['id'])

    # Update UserLab's user_id and lab_id to use UUID
    op.add_column('user_lab', sa.Column('new_user_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('user_lab', sa.Column('new_lab_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.execute('UPDATE user_lab SET new_user_id = (SELECT new_id FROM "user" WHERE "user".id = user_lab.user_id)')
    op.execute('UPDATE user_lab SET new_lab_id = (SELECT new_id FROM lab WHERE lab.id = user_lab.lab_id)')
    op.alter_column('user_lab', 'new_user_id', nullable=False)
    op.alter_column('user_lab', 'new_lab_id', nullable=False)
    op.drop_constraint('user_lab_user_id_fkey', 'user_lab', type_='foreignkey')
    op.drop_constraint('user_lab_lab_id_fkey', 'user_lab', type_='foreignkey')
    op.drop_column('user_lab', 'user_id')
    op.drop_column('user_lab', 'lab_id')
    op.alter_column('user_lab', 'new_user_id', new_column_name='user_id')
    op.alter_column('user_lab', 'new_lab_id', new_column_name='lab_id')
    op.create_foreign_key('user_lab_user_id_fkey', 'user_lab', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('user_lab_lab_id_fkey', 'user_lab', 'lab', ['lab_id'], ['id'], ondelete='CASCADE')

    # Create a new UUID column with a default UUID value for Borrowing
    op.add_column('borrowing', sa.Column('new_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')))
    op.execute('UPDATE borrowing SET new_id = uuid_generate_v4()')
    op.alter_column('borrowing', 'new_id', nullable=False)
    op.drop_column('borrowing', 'id')
    op.alter_column('borrowing', 'new_id', new_column_name='id')
    op.create_primary_key('borrowing_pkey', 'borrowing', ['id'])

    # Update Borrowing's user_id and item_id to use UUID
    op.add_column('borrowing', sa.Column('new_user_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('borrowing', sa.Column('new_item_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.execute('UPDATE borrowing SET new_user_id = (SELECT new_id FROM "user" WHERE "user".id = borrowing.user_id)')
    op.execute('UPDATE borrowing SET new_item_id = (SELECT new_id FROM item WHERE item.id = borrowing.item_id)')
    op.alter_column('borrowing', 'new_user_id', nullable=False)
    op.alter_column('borrowing', 'new_item_id', nullable=False)
    op.drop_constraint('borrowing_user_id_fkey', 'borrowing', type_='foreignkey')
    op.drop_constraint('borrowing_item_id_fkey', 'borrowing', type_='foreignkey')
    op.drop_column('borrowing', 'user_id')
    op.drop_column('borrowing', 'item_id')
    op.alter_column('borrowing', 'new_user_id', new_column_name='user_id')
    op.alter_column('borrowing', 'new_item_id', new_column_name='item_id')
    op.create_foreign_key('borrowing_user_id_fkey', 'borrowing', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('borrowing_item_id_fkey', 'borrowing', 'item', ['item_id'], ['id'], ondelete='CASCADE')


def downgrade():
    # Reverse the upgrade process
    # Drop UUID columns and recreate integer columns
    op.add_column('user', sa.Column('old_id', sa.Integer, autoincrement=True))
    op.add_column('lab', sa.Column('old_id', sa.Integer, autoincrement=True))
    op.add_column('item', sa.Column('old_id', sa.Integer, autoincrement=True))
    op.add_column('user_lab', sa.Column('old_id', sa.Integer, autoincrement=True))
    op.add_column('borrowing', sa.Column('old_id', sa.Integer, autoincrement=True))

    # Populate the old columns with default values
    # Generate sequences for the integer IDs if not exist
    op.execute('CREATE SEQUENCE IF NOT EXISTS user_id_seq AS INTEGER OWNED BY "user".old_id')
    op.execute('CREATE SEQUENCE IF NOT EXISTS lab_id_seq AS INTEGER OWNED BY lab.old_id')
    op.execute('CREATE SEQUENCE IF NOT EXISTS item_id_seq AS INTEGER OWNED BY item.old_id')
    op.execute('CREATE SEQUENCE IF NOT EXISTS user_lab_id_seq AS INTEGER OWNED BY user_lab.old_id')
    op.execute('CREATE SEQUENCE IF NOT EXISTS borrowing_id_seq AS INTEGER OWNED BY borrowing.old_id')

    op.execute('SELECT setval(\'user_id_seq\', COALESCE((SELECT MAX(old_id) + 1 FROM "user"), 1), false)')
    op.execute('SELECT setval(\'lab_id_seq\', COALESCE((SELECT MAX(old_id) + 1 FROM lab), 1), false)')
    op.execute('SELECT setval(\'item_id_seq\', COALESCE((SELECT MAX(old_id) + 1 FROM item), 1), false)')
    op.execute('SELECT setval(\'user_lab_id_seq\', COALESCE((SELECT MAX(old_id) + 1 FROM user_lab), 1), false)')
    op.execute('SELECT setval(\'borrowing_id_seq\', COALESCE((SELECT MAX(old_id) + 1 FROM borrowing), 1), false)')

    op.execute('UPDATE "user" SET old_id = nextval(\'user_id_seq\')')
    op.execute('UPDATE lab SET old_id = nextval(\'lab_id_seq\')')
    op.execute('UPDATE item SET old_id = nextval(\'item_id_seq\')')
    op.execute('UPDATE user_lab SET old_id = nextval(\'user_lab_id_seq\')')
    op.execute('UPDATE borrowing SET old_id = nextval(\'borrowing_id_seq\')')

    # Drop new columns and rename old columns back
    op.drop_constraint('lab_owner_id_fkey', 'lab', type_='foreignkey')
    op.drop_column('lab', 'owner_id')
    op.alter_column('lab', 'old_id', new_column_name='id')
    op.create_primary_key('lab_pkey', 'lab', ['id'])

    op.drop_constraint('item_lab_id_fkey', 'item', type_='foreignkey')
    op.drop_column('item', 'lab_id')
    op.alter_column('item', 'old_id', new_column_name='id')
    op.create_primary_key('item_pkey', 'item', ['id'])

    op.drop_constraint('user_lab_user_id_fkey', 'user_lab', type_='foreignkey')
    op.drop_constraint('user_lab_lab_id_fkey', 'user_lab', type_='foreignkey')
    op.drop_column('user_lab', 'user_id')
    op.drop_column('user_lab', 'lab_id')
    op.alter_column('user_lab', 'old_id', new_column_name='id')
    op.create_primary_key('user_lab_pkey', 'user_lab', ['id'])

    op.drop_constraint('borrowing_user_id_fkey', 'borrowing', type_='foreignkey')
    op.drop_constraint('borrowing_item_id_fkey', 'borrowing', type_='foreignkey')
    op.drop_column('borrowing', 'user_id')
    op.drop_column('borrowing', 'item_id')
    op.alter_column('borrowing', 'old_id', new_column_name='id')
    op.create_primary_key('borrowing_pkey', 'borrowing', ['id'])

    op.drop_column('user', 'id')
    op.alter_column('user', 'old_id', new_column_name='id')
    op.create_primary_key('user_pkey', 'user', ['id'])

    # Recreate foreign key constraints
    op.create_foreign_key('lab_owner_id_fkey', 'lab', 'user', ['owner_id'], ['id'])
    op.create_foreign_key('item_lab_id_fkey', 'item', 'lab', ['lab_id'], ['id'])
    op.create_foreign_key('user_lab_user_id_fkey', 'user_lab', 'user', ['user_id'], ['id'])
    op.create_foreign_key('user_lab_lab_id_fkey', 'user_lab', 'lab', ['lab_id'], ['id'])
    op.create_foreign_key('borrowing_user_id_fkey', 'borrowing', 'user', ['user_id'], ['id'])
    op.create_foreign_key('borrowing_item_id_fkey', 'borrowing', 'item', ['item_id'], ['id'])
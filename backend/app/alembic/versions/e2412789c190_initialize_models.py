"""Initialize models

Revision ID: e2412789c190
Revises:
Create Date: 2023-11-24 22:55:43.195942

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.reflection import Inspector
from alembic import op
from sqlmodel.sql.sqltypes import AutoString

# revision identifiers, used by Alembic.
revision = "e2412789c190"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Enable the uuid-ossp extension if it doesn't already exist
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Check if the 'user' table exists
    inspector = Inspector.from_engine(op.get_bind())
    if 'user' not in inspector.get_table_names():
        op.create_table(
            "user",
            sa.Column("email", AutoString(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default="True"),
            sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default="False"),
            sa.Column("full_name", AutoString(), nullable=True),
            sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('uuid_generate_v4()')),
            sa.Column("hashed_password", AutoString(), nullable=False),
            sa.PrimaryKeyConstraint("user_id"),
        )
        op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)

    # Check if the 'lab' table exists
    if 'lab' not in inspector.get_table_names():
        op.create_table(
            "lab",
            sa.Column("lab_place", AutoString(length=255), nullable=True),
            sa.Column("lab_university", AutoString(length=255), nullable=True),
            sa.Column("lab_num", AutoString(length=255), nullable=True),
            sa.Column("lab_id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('uuid_generate_v4()')),
            sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["owner_id"],
                ["user.user_id"],  # Corrected to reference the user table
                ondelete="CASCADE",
            ),
            sa.PrimaryKeyConstraint("lab_id"),
        )

    # Check if the 'item' table exists
    if 'item' not in inspector.get_table_names():
        op.create_table(
            "item",
            sa.Column("item_name", AutoString(length=255), nullable=False),
            sa.Column("quantity", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("item_img_url", AutoString(length=255), nullable=True),
            sa.Column("item_vendor", AutoString(length=255), nullable=True),
            sa.Column("item_params", AutoString(length=255), nullable=True),
            sa.Column("item_id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('uuid_generate_v4()')),
            sa.Column("lab_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["lab_id"],
                ["lab.lab_id"],
                name="item_lab_id_fkey",
                ondelete="CASCADE",
            ),
            sa.PrimaryKeyConstraint("item_id"),
        )

    # Check if the 'user_lab' table exists
    if 'user_lab' not in inspector.get_table_names():
        op.create_table(
            "user_lab",
            sa.Column("userlab_id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('uuid_generate_v4()')),
            sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("lab_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("can_edit_lab", sa.Boolean(), nullable=False, server_default="false"),
            sa.Column("can_edit_items", sa.Boolean(), nullable=False, server_default="false"),
            sa.Column("can_edit_users", sa.Boolean(), nullable=False, server_default="false"),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["user.user_id"],  # Corrected to reference the user table
                ondelete="CASCADE",
            ),
            sa.ForeignKeyConstraint(
                ["lab_id"],
                ["lab.lab_id"],  # Corrected to reference the lab table
                ondelete="CASCADE",
            ),
            sa.PrimaryKeyConstraint("userlab_id"),
        )

    # Check if the 'borrowing' table exists
    if 'borrowing' not in inspector.get_table_names():
        op.create_table(
            "borrowing",
            sa.Column("borrow_id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('uuid_generate_v4()')),
            sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("item_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("borrowed_at", AutoString(), nullable=False),
            sa.Column("returned_at", AutoString(), nullable=True),
            sa.Column("table_name", AutoString(), nullable=True),
            sa.Column("system_name", AutoString(), nullable=True),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["user.user_id"],  # Corrected to reference the user table
                ondelete="CASCADE",
            ),
            sa.ForeignKeyConstraint(
                ["item_id"],
                ["item.item_id"],  # Corrected to reference the item table
                ondelete="CASCADE",
            ),
            sa.PrimaryKeyConstraint("borrow_id"),
        )
    # ### end Alembic commands ###


def downgrade():
    op.drop_table("borrowing")
    op.drop_table("user_lab")
    op.drop_table("item")
    op.drop_table("lab")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###
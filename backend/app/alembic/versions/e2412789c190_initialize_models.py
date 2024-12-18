"""Initialize models

Revision ID: e2412789c190
Revises:
Create Date: 2023-11-24 22:55:43.195942

"""
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op

# revision identifiers, used by Alembic.
revision = "e2412789c190"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="True"),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default="False"),
        sa.Column("full_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)

    op.create_table(
        "lab",
        sa.Column("lab_place", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.Column("lab_university", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.Column("lab_num", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.Column("lab_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("owner_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.user_id"],  # Corrected to reference the user table
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("lab_id"),
    )

    op.create_table(
        "item",
        sa.Column("item_name", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("item_img_url", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.Column("item_vendor", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.Column("item_params", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.Column("item_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("lab_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lab_id"],
            ["lab.lab_id"],
            name="item_lab_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("item_id"),
    )

    op.create_table(
        "user_lab",
        sa.Column("userlab_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("lab_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
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

    op.create_table(
        "borrowing",
        sa.Column("borrow_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("item_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("borrowed_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("returned_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("table_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("system_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
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
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
        sa.Column("lab_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("lab_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("owner_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("lab_id"),
    )

    op.create_table(
        "item",
        sa.Column("item_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("item_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("lab_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.ForeignKeyConstraint("lab_id", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("item_id"),
    )

    op.create_table(
        "user_lab",
        sa.Column("userlab_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("lab_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["lab_id"],
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
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["item_id"],
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

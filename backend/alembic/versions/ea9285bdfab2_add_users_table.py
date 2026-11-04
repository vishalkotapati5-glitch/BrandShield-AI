
"""add users table

Revision ID: ea9285bdfab2
Revises: 0001
"""

from alembic import op
import sqlalchemy as sa


revision = "ea9285bdfab2"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("organisation_id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column(
            "role",
            sa.Enum("ADMIN", "REVIEWER", "EDITOR", name="user_role"),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["organisation_id"],
            ["organisations.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=True,
    )

    op.create_index(
        "ix_users_organisation_id",
        "users",
        ["organisation_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_users_organisation_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    # Remove the PostgreSQL role enum after dropping the users table.
    sa.Enum(name="user_role").drop(op.get_bind(), checkfirst=True)


"""add brand guidelines table

Revision ID: 12dc6fdaf2b5
Revises: ea9285bdfab2
"""

from alembic import op
import sqlalchemy as sa


revision = "12dc6fdaf2b5"
down_revision = "ea9285bdfab2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "brand_guidelines",
        sa.Column("organisation_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("rule", sa.Text(), nullable=False),
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
        "ix_brand_guidelines_organisation_id",
        "brand_guidelines",
        ["organisation_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_brand_guidelines_organisation_id",
        table_name="brand_guidelines",
    )
    op.drop_table("brand_guidelines")

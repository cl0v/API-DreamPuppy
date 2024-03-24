"""Kennel_ID will now become a column inside the puppies table

Revision ID: 611279e0d231
Revises: d1eb33d3fcca
Create Date: 2024-03-24 13:55:37.624459

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "611279e0d231"
down_revision: Union[str, None] = "d1eb33d3fcca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "puppies",
        sa.Column(
            "kennel",
            sa.Integer,
            sa.ForeignKey("kennels.id"),
            nullable=False,
            server_default=sa.text("1"),
            unique=False,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "puppies",
        "kennel",
    )

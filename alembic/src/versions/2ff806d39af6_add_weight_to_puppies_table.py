"""add Weight and Prio to puppies table

Revision ID: 2ff806d39af6
Revises:
Create Date: 2024-03-16 20:00:28.611643

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2ff806d39af6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "puppies",
        sa.Column(
            "weight",
            sa.Integer,
            doc="Puppy weight param",
            nullable=True,
        ),
    )
    op.add_column(
        "puppies",
        sa.Column(
            "prio",
            sa.Integer,
            doc="Prioritize according to defined rules to show first on gallery",
            server_default=sa.text("1"),
        ),
    )


def downgrade() -> None:
    op.drop_column("puppies", "weight")
    op.drop_column("puppies", "prio")

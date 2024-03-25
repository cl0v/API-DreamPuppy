"""Drop geo table and use lat and lon in kennels table

Revision ID: d0d46cde0a3a
Revises: 6a9c7d3a309e
Create Date: 2024-03-24 15:57:03.811818

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d0d46cde0a3a"
down_revision: Union[str, None] = "6a9c7d3a309e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Skips
    # op.drop_column("kennels", "geo")
    # op.drop_table("geo")
    op.add_column(
        "kennels",
        sa.Column(
            "lat",
            sa.Numeric,
            nullable=False,
            unique=False,
            index=True,
            server_default=sa.text('0.0'),
        ),
    )
    op.add_column(
        "kennels",
        sa.Column(
            "lon",
            sa.Numeric,
            nullable=False,
            unique=False,
            index=True,
            server_default=sa.text('0.0'),
        ),
    )


def downgrade() -> None:
    op.drop_column("kennels", "lon")
    op.drop_column("kennels", "lat")
    pass

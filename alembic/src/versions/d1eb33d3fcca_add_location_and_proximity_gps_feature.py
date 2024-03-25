"""Add location and proximity (GPS) feature

Revision ID: d1eb33d3fcca
Revises: 2ff806d39af6
Create Date: 2024-03-18 15:49:00.866999

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d1eb33d3fcca"
down_revision: Union[str, None] = "2ff806d39af6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Skips
    pass
    # op.create_table(
    #     "geo",
    #     sa.Column("id", sa.Integer, primary_key=True),
    #     sa.Column("lat", sa.Numeric, nullable=False),
    #     sa.Column("lon", sa.Numeric, nullable=False),
    # )

    # op.add_column(
    #     "kennels",
    #     sa.Column(
    #         "geo",
    #         sa.Integer,
    #         sa.ForeignKey("geo.id"),
    #         doc="Referencia a tabela de geo",
    #         nullable=True,
    #         unique=True,
    #     ),
    # )


def downgrade() -> None:
    pass

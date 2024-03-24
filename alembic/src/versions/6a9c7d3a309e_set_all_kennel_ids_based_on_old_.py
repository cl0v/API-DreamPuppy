"""Set all kennel ids based on old relation table

Revision ID: 6a9c7d3a309e
Revises: 611279e0d231
Create Date: 2024-03-24 14:07:37.000580

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6a9c7d3a309e"
down_revision: Union[str, None] = "611279e0d231"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE puppies SET kennel = (SELECT kennel_id FROM kennels_n_puppies WHERE puppies.id = kennels_n_puppies.puppy_id);
        """
    )


def downgrade() -> None:
    pass

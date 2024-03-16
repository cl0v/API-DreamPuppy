"""fix v.0.2

Revision ID: dd760d0ff6b6
Revises: de9637f72207
Create Date: 2024-02-26 10:31:04.239135

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd760d0ff6b6'
down_revision: Union[str, None] = 'de9637f72207'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text('CREATE SEQUENCE kennels_id_seq'))


def downgrade() -> None:
    op.execute(sa.text('DROP SEQUENCE kennel_id_seq'))

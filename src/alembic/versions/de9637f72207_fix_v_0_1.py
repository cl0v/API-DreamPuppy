"""fix v.0.1

Revision ID: de9637f72207
Revises: 
Create Date: 2024-02-25 23:04:58.570203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'de9637f72207'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass

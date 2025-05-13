"""merge 50e910f579c5 and f3572504bb09

Revision ID: a69a1704acd2
Revises: 50e910f579c5, f3572504bb09
Create Date: 2025-04-24 15:52:11.317088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a69a1704acd2'
down_revision: Union[str, None] = ('50e910f579c5', 'f3572504bb09')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

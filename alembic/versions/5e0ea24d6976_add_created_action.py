"""add created action

Revision ID: 5e0ea24d6976
Revises: 09cfef5a805d
Create Date: 2026-06-02 12:42:24.684510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e0ea24d6976'
down_revision: Union[str, Sequence[str], None] = '09cfef5a805d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

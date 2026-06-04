"""vehicle reservation end nullable is true

Revision ID: 00187dae9cf4
Revises: 5e0ea24d6976
Create Date: 2026-06-02 14:29:48.211307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00187dae9cf4'
down_revision: Union[str, Sequence[str], None] = '5e0ea24d6976'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

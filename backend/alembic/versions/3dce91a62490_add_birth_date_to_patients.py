"""add birth date to patients

Revision ID: 3dce91a62490
Revises: d70ca4a12526
Create Date: 2026-08-21 13:28:59.726433

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3dce91a62490"
down_revision: Union[str, Sequence[str], None] = "d70ca4a12526"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
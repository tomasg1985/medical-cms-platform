"""remove age and convert birth date to date

Revision ID: 69a19fdf25d3
Revises: 4806aec454fe
Create Date: 2026-08-27 15:51:25.647804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69a19fdf25d3'
down_revision: Union[str, Sequence[str], None] = '4806aec454fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("patients", "age")

    op.alter_column(
        "patients",
        "birth_date",
        type_=sa.Date(),
        postgresql_using="birth_date::date",
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass

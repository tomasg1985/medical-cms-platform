"""add clinic relationship to patients

Revision ID: d70ca4a12526
Revises: 
Create Date: 2026-08-18 13:52:17.820020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd70ca4a12526'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        'patients',
        sa.Column(
            'clinic_id',
            sa.Integer(),
            nullable=True,
        )
    )

    op.execute(
        "UPDATE patients SET clinic_id = 1"
    )

    op.alter_column(
        'patients',
        'clinic_id',
        nullable=False,
    )

    op.create_foreign_key(
        "fk_patients_clinic_id",
        'patients',
        'clinics',
        ['clinic_id'],
        ['id'],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "fk_patients_clinic_id",
        'patients',
        type_='foreignkey',
    )

    op.drop_column(
        'patients',
        'clinic_id',
    )
    # ### end Alembic commands ###

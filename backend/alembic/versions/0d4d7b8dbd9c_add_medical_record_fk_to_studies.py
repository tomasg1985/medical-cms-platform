"""add medical_record foreign key to studies

Revision ID: 0d4d7b8dbd9c
Revises: a9e9623db998
Create Date: 2026-10-07 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d4d7b8dbd9c'
down_revision: Union[str, Sequence[str], None] = 'a9e9623db998'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'studies',
        sa.Column('medical_record_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_studies_medical_record_id',
        'studies',
        'medical_records',
        ['medical_record_id'],
        ['id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_studies_medical_record_id', 'studies', type_='foreignkey')
    op.drop_column('studies', 'medical_record_id')

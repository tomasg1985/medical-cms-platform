
"""add modules entities

Revision ID: 01ad26dedfb1
Revises: 0d4d7b8dbd9c
Create Date: 2026-10-08 23:40:57.239002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Identificadores de la revisión de Alembic.
revision: str = '01ad26dedfb1'
down_revision: Union[str, Sequence[str], None] = '0d4d7b8dbd9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aplicar los cambios de la migración."""

    # Crear la tabla de módulos.
    op.create_table(
        'modules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Crear la tabla de tenants.
    op.create_table(
        'tenants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Crear un tenant inicial para las clínicas existentes.
    op.execute(
        sa.text("""
            INSERT INTO tenants (name, status, created_at, updated_at)
            VALUES (
                'Tenant de prueba',
                'active',
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            )
        """)
    )

    # Crear la tabla intermedia entre clínicas y módulos.
    op.create_table(
        'clinic_modules',
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('activated_at', sa.DateTime(), nullable=False),
        sa.Column('deactivated_at', sa.DateTime(), nullable=True),
        sa.Column('clinic_id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinics.id']),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id']),
        sa.PrimaryKeyConstraint('clinic_id', 'module_id')
    )

    # Agregar tenant_id temporalmente como nullable
    # para poder asignar el tenant a las clínicas existentes.
    op.add_column(
        'clinics',
        sa.Column('tenant_id', sa.Integer(), nullable=True)
    )

    # Asociar las clínicas existentes al tenant inicial.
    op.execute(
        sa.text("""
            UPDATE clinics
            SET tenant_id = (
                SELECT id
                FROM tenants
                WHERE name = 'Tenant de prueba'
            )
        """)
    )

    # Hacer obligatoria la columna una vez asignado el tenant.
    op.alter_column(
        'clinics',
        'tenant_id',
        existing_type=sa.Integer(),
        nullable=False
    )

    # Crear una única clave foránea entre clínicas y tenants.
    op.create_foreign_key(
        'fk_clinics_tenant_id_tenants',
        'clinics',
        'tenants',
        ['tenant_id'],
        ['id']
    )

    # Hacer obligatorio medical_record_id.
    op.alter_column(
        'studies',
        'medical_record_id',
        existing_type=sa.INTEGER(),
        nullable=False
    )


def downgrade() -> None:
    """Revertir los cambios de la migración."""

    # Restaurar la nulabilidad original de medical_record_id.
    op.alter_column(
        'studies',
        'medical_record_id',
        existing_type=sa.INTEGER(),
        nullable=True
    )

    # Eliminar la clave foránea y la columna tenant_id.
    op.drop_constraint(
        'fk_clinics_tenant_id_tenants',
        'clinics',
        type_='foreignkey'
    )

    op.drop_column('clinics', 'tenant_id')

    # Eliminar las tablas creadas por la migración.
    op.drop_table('clinic_modules')
    op.drop_table('tenants')
    op.drop_table('modules')

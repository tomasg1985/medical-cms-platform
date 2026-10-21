from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.clinic_model import Clinic
    from app.models.audit_logs_model import AuditLog
    from app.models.system_logs_model import SystemLog


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

    clinics: Mapped[list["Clinic"]] = relationship(
        back_populates="tenant"
    )
    
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        back_populates="tenant"
    )
    
    system_logs: Mapped[list["SystemLog"]] = relationship(
        back_populates="tenant"
    )
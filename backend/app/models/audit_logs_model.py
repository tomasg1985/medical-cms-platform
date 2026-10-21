from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base

if TYPE_CHECKING:
    from app.models.tenant_model import Tenant
    from app.models.clinic_model import Clinic
    from app.models.user_model import User

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(nullable=False)
    resource_type: Mapped[str] = mapped_column(nullable=False)
    resource_id: Mapped[str] = mapped_column(nullable=True)
    outcome: Mapped[str] = mapped_column(nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(nullable=False)
    ip_address: Mapped[str] = mapped_column(nullable=True)
    user_agent: Mapped[str] = mapped_column(nullable=True)
    request_id: Mapped[str] = mapped_column(nullable=True)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict, nullable=False)
    
    
    tenant: Mapped["Tenant | None"] = relationship(
        back_populates="audit_logs"
    )

    clinic: Mapped["Clinic | None"] = relationship(
        back_populates="audit_logs"
    )

    user: Mapped["User | None"] = relationship(
        back_populates="audit_logs"
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=True
    )
    
    clinic_id: Mapped[int] = mapped_column(
        ForeignKey("clinics.id"),
        nullable=True
    )
    
    actor_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )
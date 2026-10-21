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

class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[str] = mapped_column(nullable=False)
    event_type: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    source: Mapped[str] = mapped_column(nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(nullable=False)
    request_id: Mapped[str] = mapped_column(nullable=True)
    correlation_id: Mapped[str] = mapped_column(nullable=True)
    exception_type: Mapped[str] = mapped_column(nullable=True)
    stack_trace: Mapped[str] = mapped_column(nullable=True)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict, nullable=False)
    
    tenant: Mapped["Tenant | None"] = relationship(
        back_populates="system_logs"
    )
    
    clinic: Mapped["Clinic | None"] = relationship(
        back_populates="system_logs"
    )
    
    user: Mapped["User | None"] = relationship(
        back_populates="system_logs"
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
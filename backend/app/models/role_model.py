from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.professional_model import Professional
    from app.models.patient_model import Patient
    from app.models.clinic_model import Clinic
    from app.models.user_model import User
    from app.models.permission_model import Permission


class Role(Base):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)
    
    users: Mapped[list["User"]] = relationship(
        secondary="user_roles",
        back_populates="roles"
    )

    permissions: Mapped[list["Permission"]] = relationship(
        secondary="role_permissions",
        back_populates="roles"
    )
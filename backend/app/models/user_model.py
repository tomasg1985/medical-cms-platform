from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.professional_model import Professional
    from app.models.patient_model import Patient
    from app.models.clinic_model import Clinic
    from app.models.role_model import Role

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)


    professional: Mapped["Professional"] = relationship(
            back_populates="user"
        )
    
    patient: Mapped["Patient"] = relationship(
        back_populates="user"
    )
    
    clinics: Mapped[list["Clinic"]] = relationship(
        secondary="user_clinics",
        back_populates="users"
    )
    
    roles: Mapped[list["Role"]] =relationship(
        secondary="user_roles",
        back_populates="users"
    )
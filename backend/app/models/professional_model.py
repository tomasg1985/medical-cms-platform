from typing import TYPE_CHECKING

from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.clinic_model import Clinic
    from app.models.specialty_model import Specialty
    from app.models.appointment_model import Appointment
    from app.models.user_model import User
    from app.models.schedule_availability_model import ScheduleAvailability

class Professional(Base):
    __tablename__ = "professionals"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    credential: Mapped[str] = mapped_column(nullable=False)
    credential_expiration: Mapped[date] = mapped_column(Date, nullable=False)
    dni: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    medical_facility: Mapped[str] = mapped_column(nullable=False)
    working_insurance: Mapped[str] = mapped_column(nullable=False)
    
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=True,
        unique=True
    )
    
    user: Mapped["User"] = relationship(
        back_populates="professional"
    )

    clinics: Mapped[list["Clinic"]] = relationship(
        secondary="professional_clinics",
        back_populates="professionals"
    )

    specialties: Mapped[list["Specialty"]] = relationship(
                    secondary="professional_specialties",
                    back_populates="professionals"
                )
    
    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="professional"
    )
    
    schedule_availabilities: Mapped[list["ScheduleAvailability"]] = relationship(
        back_populates="professional"
    )
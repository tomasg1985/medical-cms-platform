from typing import TYPE_CHECKING

from datetime import date, time

from sqlalchemy import Date, ForeignKey, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.appointment_model import Appointment
    from app.models.clinic_model import Clinic
    from app.models.specialty_model import Specialty
    from app.models.professional_model import Professional

class ScheduleAvailability(Base):
    __tablename__ = "schedule_availabilities"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    weekday: Mapped[int] = mapped_column(nullable=False)
    start_hour: Mapped[time] = mapped_column(Time, nullable=False)
    end_hour: Mapped[time] = mapped_column(Time, nullable=False)
    consulting_duration: Mapped[int] = mapped_column(nullable=False)
    valid_from: Mapped[date] = mapped_column(Date, nullable=False)
    valid_until: Mapped[date] = mapped_column(Date, nullable=True)
    activity_status: Mapped[str] = mapped_column(nullable=False)


    professional_id: Mapped[int] = mapped_column(
        ForeignKey("professionals.id"),
        nullable=False
    )

    clinic_id: Mapped[int] = mapped_column(
        ForeignKey("clinics.id"),
        nullable=False
    )

    specialty_id: Mapped[int] = mapped_column(
        ForeignKey("specialties.id"),
        nullable=False
    )

    professional: Mapped["Professional"] = relationship(
        back_populates="schedule_availabilities"
    )

    clinic: Mapped["Clinic"] = relationship(
        back_populates="schedule_availabilities"
    )

    specialty: Mapped["Specialty"] = relationship(
        back_populates="schedule_availabilities"
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="schedule_availability"
    )
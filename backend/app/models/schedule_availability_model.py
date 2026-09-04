from datetime import date, time

from sqlalchemy import Date, ForeignKey, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

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
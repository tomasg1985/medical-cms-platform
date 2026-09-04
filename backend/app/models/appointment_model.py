from datetime import date, time
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Appointment(Base):
    __tablename__ = "appointments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    reservation_code: Mapped[str] = mapped_column(nullable=False, unique=True)
    appointment_date: Mapped[date] = mapped_column(Date, nullable=False)
    appointment_hour: Mapped[time] = mapped_column(Time, nullable=False)
    consulting_duration: Mapped[int] = mapped_column(nullable=False)
    consulting_mode: Mapped[str] = mapped_column(nullable=False)
    appointment_state: Mapped[str] = mapped_column(nullable=False)
    consulting_reason: Mapped[str] = mapped_column(nullable=True)
    cancelation_reason: Mapped[str] = mapped_column(nullable=True)
    amount_paid: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    payment_status: Mapped[str] = mapped_column(nullable=False)


    clinic_id: Mapped[int] = mapped_column(
        ForeignKey("clinics.id"),
        nullable=False
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False
    )

    professional_id: Mapped[int] = mapped_column(
        ForeignKey("professionals.id"),
        nullable=False
    )

    specialty_id: Mapped[int] = mapped_column(
        ForeignKey("specialties.id"),
        nullable=False
    )

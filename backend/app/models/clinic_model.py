from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.patient_model import Patient
    from app.models.professional_model import Professional
    from app.models.specialty_model import Specialty
    from app.models.appointment_model import Appointment
    from app.models.schedule_availability_model import ScheduleAvailability

class Clinic(Base):
    __tablename__ = "clinics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    
    patients: Mapped[list["Patient"]] = relationship(
        secondary="patient_clinics",
        back_populates="clinics"
    )
    
    professionals: Mapped[list["Professional"]] = relationship(
        secondary="professional_clinics",
        back_populates="clinics"
    )
    
    specialties: Mapped[list["Specialty"]] = relationship(
                secondary="clinic_specialties",
                back_populates="clinics"
            )
    
    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="clinic"
    )
    
    schedule_availabilities: Mapped[list["ScheduleAvailability"]] = relationship(
        back_populates="clinic"
    )
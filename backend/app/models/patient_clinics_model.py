from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from sqlalchemy import ForeignKey

class PatientClinic(Base):
    __tablename__ = "patient_clinics"
    
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False,
        primary_key=True
    )

    clinic_id: Mapped[int] = mapped_column(
        ForeignKey("clinics.id"),
        nullable=False,
        primary_key=True
    )
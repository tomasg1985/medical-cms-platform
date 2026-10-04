from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.patient_model import Patient
    from app.models.clinic_model import Clinic

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    __table_args__ = (
        UniqueConstraint("patient_id", "clinic_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False
    )

    clinic_id: Mapped[int] = mapped_column(
            ForeignKey("clinics.id"),
            nullable=False
        )

    patient: Mapped["Patient"] = relationship(
        back_populates="medical_records"
    )

    clinic: Mapped["Clinic"] = relationship(
        back_populates="medical_records"
    )
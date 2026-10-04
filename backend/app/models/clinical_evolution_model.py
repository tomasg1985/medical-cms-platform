from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.medical_record_model import MedicalRecord
    from app.models.professional_model import Professional
    from app.models.appointment_model import Appointment


class ClinicalEvolution(Base):
    __tablename__ = "clinical_evolutions"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

    medical_record_id: Mapped[int] = mapped_column(
        ForeignKey("medical_records.id"),
        nullable=False
    )

    professional_id: Mapped[int] = mapped_column(
        ForeignKey("professionals.id"),
        nullable=False
    )

    appointment_id: Mapped[int] = mapped_column(
        ForeignKey("appointments.id"),
        nullable=False
    )

    medical_record: Mapped["MedicalRecord"] = relationship(
        back_populates="clinical_evolutions"
    )

    professional: Mapped["Professional"] = relationship(
        back_populates="clinical_evolutions"
    )
    
    appointment: Mapped["Appointment"] = relationship(
        back_populates="clinical_evolutions"
    )
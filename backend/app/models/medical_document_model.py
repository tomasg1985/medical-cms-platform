from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.patient_model import Patient
    from app.models.medical_record_model import MedicalRecord
    from app.models.professional_model import Professional
    from app.models.clinic_model import Clinic

class MedicalDocument(Base):
    __tablename__ = "medical_documents"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)
    document_type: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)


    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False
    )

    medical_record_id: Mapped[int] = mapped_column(
        ForeignKey("medical_records.id"),
        nullable=False
    )

    professional_id: Mapped[int] = mapped_column(
        ForeignKey("professionals.id"),
        nullable=False
    )

    clinic_id: Mapped[int] = mapped_column(
        ForeignKey("clinics.id"),
        nullable=False
    )

    patient: Mapped["Patient"] = relationship(
        back_populates="medical_documents"
    )

    medical_record: Mapped["MedicalRecord"] = relationship(
        back_populates="medical_documents"
    )

    professional: Mapped["Professional"] = relationship(
        back_populates="medical_documents"
    )

    clinic: Mapped["Clinic"] = relationship(
        back_populates="medical_documents"
    )
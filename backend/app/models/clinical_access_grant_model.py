from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.patient_model import Patient
    from app.models.clinic_model import Clinic
    from app.models.professional_model import Professional
    from app.models.appointment_model import Appointment
    from app.models.clinical_access_grant_scope_model import ClinicalAccessGrantScope

class ClinicalAccessGrant(Base):
    __tablename__ = "clinical_access_grants"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(nullable=False)
    requested_at: Mapped[datetime] = mapped_column(nullable=False)
    granted_at: Mapped[datetime] = mapped_column(nullable=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=True)
    revoked_at: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)


    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
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
    
    appointment_id: Mapped[int] = mapped_column(
        ForeignKey("appointments.id"),
        nullable=True
    )
    
    patient: Mapped["Patient"] = relationship(
        back_populates="clinical_access_grants"
    )
    
    professional: Mapped["Professional"] = relationship(
        back_populates="clinical_access_grants"
    )
    
    clinic: Mapped["Clinic"] = relationship(
        back_populates="clinical_access_grants"
    )
    
    appointment: Mapped["Appointment"] = relationship(
        back_populates="clinical_access_grants"
    )
    
    clinical_access_grant_scopes: Mapped[list["ClinicalAccessGrantScope"]] = relationship(
        back_populates="clinical_access_grant"
    )
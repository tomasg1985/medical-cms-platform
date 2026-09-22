from typing import TYPE_CHECKING

from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.patient_model import Patient
    from app.models.insurance_plan_model import InsurancePlan

class PatientInsurancePlan(Base):
    __tablename__ = "patient_insurance_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    policy_number: Mapped[str] = mapped_column(nullable=False)
    is_primary: Mapped[bool] = mapped_column(nullable=False)
    expiration_date: Mapped[date] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False
    )
    
    insurance_plan_id: Mapped[int] = mapped_column(
            ForeignKey("insurance_plans.id"),
            nullable=False
        )
    
    patient: Mapped["Patient"] = relationship(
        back_populates="patient_insurance_plans"
    )

    insurance_plan: Mapped["InsurancePlan"] = relationship(
        back_populates="patient_insurance_plans"
    )
    
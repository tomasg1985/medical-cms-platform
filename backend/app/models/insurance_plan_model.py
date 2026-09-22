from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.insurance_model import Insurance
    from app.models.plan_model import Plan
    from app.models.patient_insurance_plan_model import PatientInsurancePlan

class InsurancePlan(Base):
    __tablename__ = "insurance_plans"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    insurance_id: Mapped[int] = mapped_column(
        ForeignKey("insurances.id"),
        nullable=False
    )
    
    plan_id: Mapped[int] = mapped_column(
        ForeignKey("plans.id"),
        nullable=False
    )
    
    plan: Mapped["Plan"] = relationship(
        back_populates="insurance_plans"
    )
    
    insurance: Mapped["Insurance"] = relationship(
        back_populates="insurance_plans"
    )
    
    patient_insurance_plans: Mapped[list["PatientInsurancePlan"]] = relationship(
        back_populates="insurance_plan"
    )
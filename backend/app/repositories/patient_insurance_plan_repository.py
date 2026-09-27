from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.patient_insurance_plan_model import PatientInsurancePlan


class PatientInsurancePlanRepository:

    def create(self, db: Session, patient_insurance_plan: PatientInsurancePlan) -> PatientInsurancePlan:
        try:
            db.add(patient_insurance_plan)
            db.commit()
            db.refresh(patient_insurance_plan)
            
            return patient_insurance_plan
        except Exception:
            db.rollback()
            raise


    def get_by_patient_insurance_plan(
    self,
    db: Session,
    patient_id: int,
    insurance_plan_id: int
    ) -> PatientInsurancePlan | None:

        statement = select(PatientInsurancePlan).where(
            PatientInsurancePlan.patient_id == patient_id,
            PatientInsurancePlan.insurance_plan_id == insurance_plan_id
        )
        result = db.execute(statement)
        patient_insurance_plan = result.scalar_one_or_none()
        
        return patient_insurance_plan


    def delete(self, db: Session, patient_insurance_plan: PatientInsurancePlan) -> bool:
            try:
                db.delete(patient_insurance_plan)
                db.commit()
                
                return True
            
            except Exception:
                db.rollback()
                raise
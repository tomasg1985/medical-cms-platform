from sqlalchemy.orm import Session

from app.models.patient_insurance_plan_model import PatientInsurancePlan

from app.repositories.patient_insurance_plan_repository import PatientInsurancePlanRepository
from app.repositories.patient_repository import PatientRepository
from app.repositories.insurance_repository import InsuranceRepository
from app.repositories.plan_repository import PlanRepository

patient_insurance_plan_repository = PatientInsurancePlanRepository()
patient_repository =  PatientRepository()
insurance_repository = InsuranceRepository()
plan_repository = PlanRepository()

def create_patient_insurance_plan(
    db: Session,
    patient_id: int,
    insurance_id: int,
    plan_id: int
) -> PatientInsurancePlan | None:
    
    patient = patient_repository.get_by_id(
        db=db,
        patient_id=patient_id
    )
    
    if patient is None:
        return None
    
    insurance = insurance_repository.get_by_id(
        db=db,
        insurance_id=insurance_id
    )
    
    if insurance is None:
        return None
    
    plan = plan_repository.get_by_id(
        db=db,
        plan_id=plan_id
    )
    
    if plan is None:
        return None
    
    existing = patient_insurance_plan_repository.get_by_patient_insurance_plan(
        db=db,
        patient_id=patient_id,
        insurance_id=insurance_id,
        plan_id=plan_id
    )
    
    if existing is not None:
        return None
    
    patient_insurance_plan = PatientInsurancePlan(
        patient_id=patient_id,
        insurance_id=insurance_id,
        plan_id=plan_id
    )
    
    patient_insurance_plan = patient_insurance_plan_repository.create(
        db=db,
        patient_insurance_plan=patient_insurance_plan
    )
    
    return patient_insurance_plan


from sqlalchemy.orm import Session

from app.models.insurance_plan_model import InsurancePlan

from app.repositories.insurance_plan_repository import InsurancePlanRepository
from app.repositories.insurance_repository import InsuranceRepository
from app.repositories.plan_repository import PlanRepository

from app.core.exceptions import InsuranceNotFoundException, PlanNotFoundException, InsurancePlanAlreadyExistsException, InsurancePlanNotFoundException

insurance_plan_repository = InsurancePlanRepository()
insurance_repository = InsuranceRepository()
plan_repository = PlanRepository()

def create_insurance_plan(
    db: Session,
    insurance_id: int,
    plan_id: int
) -> InsurancePlan:
    
    insurance = insurance_repository.get_by_id(
        db=db,
        insurance_id=insurance_id
    )

    if insurance is None:
        raise InsuranceNotFoundException()

    plan = plan_repository.get_by_id(
        db=db,
        plan_id=plan_id
    )

    if plan is None:
        raise PlanNotFoundException()


    existing = insurance_plan_repository.get_by_insurance_and_plan_name(
        db=db,
        insurance_id=insurance_id,
        plan_name=plan.name
    )
    
    if existing is not None:
        raise InsurancePlanAlreadyExistsException()
    
    insurance_plan = InsurancePlan(
        insurance_id=insurance_id,
        plan_id=plan_id
    )
    
    insurance_plan = insurance_plan_repository.create(
        db=db,
        insurance_plan=insurance_plan
    )
    
    return insurance_plan


def get_insurance_plans(db: Session) -> list[InsurancePlan]:
    
    insurance_plans = insurance_plan_repository.get_insurance_plans(
        db=db
    )
    
    return insurance_plans


def get_insurance_plan(db: Session, insurance_plan_id: int) -> InsurancePlan:
    
    insurance_plan = insurance_plan_repository.get_by_id(
        db=db,
        insurance_plan_id=insurance_plan_id
    )
    
    if insurance_plan is None:
        raise InsurancePlanNotFoundException()
    
    return insurance_plan
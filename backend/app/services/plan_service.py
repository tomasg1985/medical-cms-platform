from sqlalchemy.orm import Session

from app.models.plan_model import Plan
from app.repositories.plan_repository import PlanRepository
from app.schemas.plan_schema import PlanUpdate

plan_repository = PlanRepository()


def create_plan(
    db: Session,
    name: str,
    description: str
) -> Plan:
    
    plan = Plan(
        name=name,
        description=description,
        is_active=True
    )
    
    plan = plan_repository.create(
        db=db,
        plan=plan
    )
    
    return plan

def get_plans(
    db: Session
) -> list[Plan]:
    
    plans = plan_repository.get_plans(
        db=db
    )
    
    return plans

def get_plan(
    db: Session,
    plan_id: int
) -> Plan | None:
    
    plan = plan_repository.get_by_id(
        db=db,
        plan_id=plan_id
    )
    
    return plan

def update_plan(
    db: Session,
    plan_id: int,
    plan_data: PlanUpdate
) -> Plan | None:
    
    plan = get_plan(
        db=db,
        plan_id=plan_id
    )
    
    if plan is None:
        return None
    
    plan.name = plan_data.name
    plan.description = plan_data.description

    plan = plan_repository.update(
        db=db,
        plan=plan
    )
    
    return plan

def delete_plan(
    db: Session,
    plan_id: int
) -> bool:
    
    plan = plan_repository.get_by_id(
        db=db,
        plan_id=plan_id
    )
    
    if plan is None:
        return False
    
    return plan_repository.delete(
        db=db,
        plan=plan
    )
    
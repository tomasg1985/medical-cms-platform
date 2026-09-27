from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.plan_schema import PlanCreate, PlanResponse, PlanUpdate
from app.services.plan_service import create_plan, get_plan, get_plans, update_plan, delete_plan

from app.core.exceptions import PlanNotFoundException

router = APIRouter(
    prefix="/plans",
    tags=["Plans"],
)

@router.post("/",response_model=PlanResponse)
def create_plan_endpoint(
    plan_data: PlanCreate,
    db: Session = Depends(get_db),
):
    
    plan = create_plan(
        db=db,
        name=plan_data.name,
        description=plan_data.description
    )
    
    return plan

@router.get("/", response_model=list[PlanResponse])
def create_plans_endpoint(
    db: Session = Depends(get_db),
):
    plans = get_plans(db)
    
    return plans


@router.get(
    "/{plan_id}", 
    response_model=PlanResponse,
    responses={
        404: {
            "description": "No se encontró ningún plan asociado al seguro"
        }
    },
)
def get_plan_endpoint(
    plan_id: int,
    db: Session = Depends(get_db),
):
    try:
        plan = get_plan(
            db=db,
            plan_id=plan_id
        )
        
        if plan is None:
            raise HTTPException(
                status_code=404,
                detail="No se encontró el seguro solicitado.",
            )
    
        return plan
    except PlanNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el seguro solicitado.",
        )


@router.put(
    "/{plan_id}",
    response_model=PlanResponse,
    responses={
        404: {
            "description": "No se encontró ningún plan asociado al seguro"
        }
    },
)
def update_plan_endpoint(
    plan_id: int,
    plan_data: PlanUpdate,
    db: Session = Depends(get_db),
):
    
    plan = update_plan(
        db=db,
        plan_id=plan_id,
        plan_data=plan_data
    )
    
    if plan is None:
        return None
    
    return plan


@router.delete(
    "/{plan_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ningún plan asociado al seguro"
        }
    },
)
def delete_plan_endpoint(
    plan_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_plan(
        db=db,
        plan_id=plan_id,
    )
    
    if not deleted:
        return None
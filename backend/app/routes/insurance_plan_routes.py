from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.insurance_plan_schema import InsurancePlanCreate, InsurancePlanResponse
from app.services.insurance_plan_service import create_insurance_plan, get_insurance_plans, get_insurance_plan

from app.core.exceptions import InsurancePlanAlreadyExistsException, InsuranceNotFoundException, PlanNotFoundException, InsurancePlanNotFoundException


router = APIRouter(
    prefix="/insurance-plans",
    tags=["Insurance Plan"]
)

@router.post(
    "/",
    response_model=InsurancePlanResponse
)
def create_insurance_plan_endpoint(
    insurance_plan_data: InsurancePlanCreate,
    db: Session = Depends(get_db),
):
    
    try:
        insurance_plan = create_insurance_plan(
            db=db,
            insurance_id=insurance_plan_data.insurance_id,
            plan_id=insurance_plan_data.plan_id
        )
        
        return insurance_plan
    except InsurancePlanAlreadyExistsException:
        raise HTTPException(
            status_code=409,
            detail="El plan ya está asociado a este seguro."
        )
    except InsuranceNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el seguro solicitado."
        )
    except PlanNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el plan solicitado."
        )


@router.get("/", response_model=list[InsurancePlanResponse])
def get_insurance_plans_endpoint(
    db: Session = Depends(get_db),
):
    return get_insurance_plans(db)


@router.get(
    "/{insurance_plan_id}",
    response_model=InsurancePlanResponse,
    responses={
        404: {
            "description": "No se encontro ningún seguro asociado al plan solicitado. "
        }
    },
)
def get_insurance_plan_endpoint(
    insurance_plan_id: int,
    db: Session = Depends(get_db)
):
    try:
        insurance_plan = get_insurance_plan(
            db=db,
            insurance_plan_id=insurance_plan_id
        )
        return insurance_plan
    except InsurancePlanNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la asociación de seguro y plan solicitada."
        )
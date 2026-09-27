from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.insurance_schema import InsuranceCreate, InsuranceResponse, InsuranceUpdate
from app.services.insurance_service import create_insurance, delete_insurance, get_insurance, get_insurances, update_insurance
from app.core.exceptions import InsuranceAlreadyExistsException, InsuranceDeleteConflictException, InsuranceNotFoundException


router = APIRouter(
    prefix="/insurances",
    tags=["Insurances"],
)


@router.post(
    "/",
    response_model=InsuranceResponse,
    status_code=201,
)
def create_insurance_endpoint(
    insurance_data: InsuranceCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_insurance(
            db=db,
            name=insurance_data.name,
            registration=insurance_data.registration,
        )
    except InsuranceAlreadyExistsException:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un seguro con esos datos.",
        )


@router.get("/", response_model=list[InsuranceResponse])
def get_insurances_endpoint(
    db: Session = Depends(get_db),
):
    return get_insurances(db)


@router.get(
    "/{insurance_id}",
    response_model=InsuranceResponse,
    responses={
        404: {
            "description": "No se encontró ningún seguro"
        }
    },
)
def get_insurance_endpoint(
    insurance_id: int,
    db: Session = Depends(get_db),
):
    try:
        insurance = get_insurance(db=db, insurance_id=insurance_id)
        if insurance is None:
            raise HTTPException(
                status_code=404,
                detail="No se encontró el seguro solicitado.",
            )
        return insurance
    except InsuranceNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el seguro solicitado.",
        )


@router.put(
    "/{insurance_id}",
    response_model=InsuranceResponse,
    responses={
        404: {
            "description": "No se encontró ningún seguro"
        }
    },
)
def update_insurance_endpoint(
    insurance_id: int,
    insurance_data: InsuranceUpdate,
    db: Session = Depends(get_db),
):
    try:
        insurance = update_insurance(
            db=db,
            insurance_id=insurance_id,
            insurance_data=insurance_data,
        )
        if insurance is None:
            raise HTTPException(
                status_code=404,
                detail="No se encontró el seguro a actualizar.",
            )
        return insurance
    except InsuranceAlreadyExistsException:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un seguro con ese número de registro.",
        )
    except InsuranceNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el seguro a actualizar.",
        )


@router.delete(
    "/{insurance_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ningún seguro"
        },
        409: {
            "description": "El seguro no se puede eliminar por dependencias"
        },
    },
)
def delete_insurance_endpoint(
    insurance_id: int,
    db: Session = Depends(get_db),
):
    try:
        delete_insurance(db=db, insurance_id=insurance_id)
    except InsuranceNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el seguro a eliminar.",
        )
    except InsuranceDeleteConflictException:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el seguro porque tiene planes asociados.",
        )
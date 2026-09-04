from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.specialty_schema import SpecialtyCreate, SpecialtyResponse, SpecialtyUpdate
from app.services.specialty_service import create_specialty, get_specialty, get_specialties, update_specialty, delete_specialty

from app.core.exceptions import SpecialtySNOMEDAlreadyExistsError


router = APIRouter(
    prefix="/specialties",
    tags=["Specialty"],
)


@router.post(
    "/", 
    response_model=SpecialtyResponse,
    responses={
        409: {
            "description": "El código de la especialidad médica ya se encuentra registrado"
        }
    },
)
def create_specialty_endpoint(
    specialty_data: SpecialtyCreate,
    db: Session = Depends(get_db),
):
    try:
        specialty = create_specialty(
            db=db,
            specialty_data=specialty_data
        )
        
        return specialty
    except SpecialtySNOMEDAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="El código de la especialidad médica ya se encuentra registrado"
            )




@router.get("/", response_model=list[SpecialtyResponse])
def get_specialties_endpoint(
    db: Session = Depends(get_db),
):
    
    specialties = get_specialties(
        db=db
    )
    
    return specialties



@router.get(
    "/{specialty_id}",
    response_model=SpecialtyResponse,
    responses={
        404: {
            "description": "No se encontró la especialidad solicitada"
        }
    },
)

def get_specialty_endpoint(
    specialty_id: int,
    db: Session = Depends(get_db),
):
    specialty = get_specialty(
        db=db,
        specialty_id=specialty_id,
    )
    
    if specialty is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la especialidad solicitada"
        )
    
    return specialty



@router.put(
    "/{specialty_id}",
    response_model=SpecialtyResponse,
    responses={
        404: {
            "description": "No se encontró la especialidad solicitada",
        }
    },
)
def update_specialty_endpoint(
    specialty_id: int,
    specialty_data: SpecialtyUpdate,
    db: Session = Depends(get_db),
):
    try:
        specialty = update_specialty(
            db=db,
            specialty_id=specialty_id,
            specialty_data=specialty_data
        )
    except SpecialtySNOMEDAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="El código de la especialidad médica ya se encuentra registrado"
            )
    
    return specialty


@router.delete(
    "/{specialty_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró la especialidad solicitada",
        }
    },
)
def delete_specialty_endpoint(
    specialty_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_specialty(
        db=db,
        specialty_id=specialty_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la especialidad solicitada",
        )
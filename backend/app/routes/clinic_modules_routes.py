
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.clinic_modules_schema import (
    ClinicModuleCreate,
    ClinicModuleUpdate,
    ClinicModuleResponse,
)
from app.services.clinic_modules_service import (
    create_clinic_module,
    get_clinic_module,
    get_clinic_modules,
    update_clinic_module,
    delete_clinic_module,
)

router = APIRouter(
    prefix="/clinic_modules",
    tags=["Clinic Modules"]
)


@router.post("/", response_model=ClinicModuleResponse, status_code=201)
def create_clinic_module_endpoint(
    clinic_module_data: ClinicModuleCreate,
    db: Session = Depends(get_db)
):
    clinic_module = create_clinic_module(
        db=db,
        clinic_module_data=clinic_module_data
    )

    if clinic_module is None:
        raise HTTPException(
            status_code=404,
            detail="La clínica o el módulo especificado no existe."
        )

    return clinic_module


@router.get("/", response_model=list[ClinicModuleResponse])
def get_clinic_modules_endpoint(
    db: Session = Depends(get_db)
):
    return get_clinic_modules(db=db)


@router.get(
    "/{clinic_id}/{module_id}",
    response_model=ClinicModuleResponse
)
def get_clinic_module_endpoint(
    clinic_id: int,
    module_id: int,
    db: Session = Depends(get_db)
):
    clinic_module = get_clinic_module(
        db=db,
        clinic_id=clinic_id,
        module_id=module_id
    )

    if clinic_module is None:
        raise HTTPException(
            status_code=404,
            detail="La asociación entre la clínica y el módulo no existe."
        )

    return clinic_module


@router.put(
    "/{clinic_id}/{module_id}",
    response_model=ClinicModuleResponse
)
def update_clinic_module_endpoint(
    clinic_id: int,
    module_id: int,
    clinic_module_data: ClinicModuleUpdate,
    db: Session = Depends(get_db)
):
    try:
        clinic_module = update_clinic_module(
            db=db,
            clinic_id=clinic_id,
            module_id=module_id,
            clinic_module_data=clinic_module_data
        )
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

    if clinic_module is None:
        raise HTTPException(
            status_code=404,
            detail="La asociación entre la clínica y el módulo no existe."
        )

    return clinic_module


@router.delete(
    "/{clinic_id}/{module_id}",
    status_code=204
)
def delete_clinic_module_endpoint(
    clinic_id: int,
    module_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_clinic_module(
        db=db,
        clinic_id=clinic_id,
        module_id=module_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="La asociación entre la clínica y el módulo no existe."
        )

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import ModuleAlreadyExistsException, ModuleNotFoundException
from app.database import get_db
from app.schemas.module_schema import ModuleCreate, ModuleUpdate, ModuleResponse
from app.services.module_service import create_module, get_module, get_modules, update_module, delete_module

router = APIRouter(
    prefix="/modules",
    tags=["Modules"],
)

@router.post(
    "/",
    response_model=ModuleResponse,
    status_code=201,
)
def create_module_endpoint(
    module_data: ModuleCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_module(
            db=db,
            module_data=module_data,
        )
    except ModuleAlreadyExistsException:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un módulo con ese nombre. Prueba con otro nombre.",
        )


@router.get("/", response_model=list[ModuleResponse])
def get_modules_endpoint(
    db: Session = Depends(get_db),
):
    return get_modules(db=db)


@router.get("/{module_id}", response_model=ModuleResponse)
def get_module_endpoint(
    module_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_module(
            db=db,
            module_id=module_id,
        )
    except ModuleNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No encontramos el módulo solicitado.",
        )


@router.put("/{module_id}", response_model=ModuleResponse)
def update_module_endpoint(
    module_id: int,
    module_data: ModuleUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update_module(
            db=db,
            module_id=module_id,
            module_data=module_data,
        )
    except ModuleAlreadyExistsException:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un módulo con ese nombre. Prueba con otro nombre.",
        )
    except ModuleNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No encontramos el módulo solicitado.",
        )


@router.delete("/{module_id}", status_code=204)
def delete_module_endpoint(
    module_id: int,
    db: Session = Depends(get_db),
):
    try:
        delete_module(
            db=db,
            module_id=module_id,
        )
    except ModuleNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No encontramos el módulo solicitado.",
        )

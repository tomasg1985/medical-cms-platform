from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.role_schema import RoleCreate, RoleResponse, RoleUpdate
from app.services.role_service import create_role, get_role, get_roles, update_role, delete_role


router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)

@router.post("/", response_model=RoleResponse)
def create_role_endpoint(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
):
    
    role = create_role(
        db=db,
        name=role_data.name,
        description=role_data.description
    )
    
    return role


@router.get("/", response_model=list[RoleResponse])
def get_roles_endpoint(
    db: Session = Depends(get_db),
):

    roles = get_roles(db)

    return roles


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    responses={
        404: {
            "description": "No se encontró ningún rol de usuario"
        }
    },
)
def get_role_endpoint(
    role_id: int,
    db: Session = Depends(get_db),
):

    role = get_role(
        db=db,
        role_id=role_id,
    )
    
    if role is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún rol de usuario",
        )
        
    return role


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    responses={
        404: {
            "description": "No se encontró ningún rol de usuario",
        }
    },
)
def update_role_endpoint(
    role_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
):

    role = update_role(
        db=db,
        role_id=role_id,
        role_data=role_data,
    )

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún rol de usuario",
        )

    return role


@router.delete(
    "/{role_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ningún rol de usuario",
        }
    },
)
def delete_role_endpoint(
    role_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_role(
        db=db,
        role_id=role_id,
    )
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún rol de usuario",
        )
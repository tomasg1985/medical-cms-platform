from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.permission_schema import PermissionCreate, PermissionResponse, PermissionUpdate
from app.services.permission_service import create_permission, get_permission, get_permissions, update_permission, delete_permission


router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)

@router.post("/", response_model=PermissionResponse)
def create_permission_endpoint(
    permission_data: PermissionCreate,
    db: Session = Depends(get_db),
):
    
    permission = create_permission(
        db=db,
        name=permission_data.name,
        description=permission_data.description,
        resource=permission_data.resource,
        action=permission_data.action
    )
    
    return permission


@router.get("/", response_model=list[PermissionResponse])
def get_permissions_endpoint(
    db: Session = Depends(get_db),
):

    permissions = get_permissions(db)

    return permissions


@router.get(
    "/{permission_id}",
    response_model=PermissionResponse,
    responses={
        404: {
            "description": "No se encontró ningún permiso de usuario"
        }
    },
)
def get_permission_endpoint(
    permission_id: int,
    db: Session = Depends(get_db),
):

    permission = get_permission(
        db=db,
        permission_id=permission_id,
    )
    
    if permission is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún permiso de usuario",
        )
        
    return permission


@router.put(
    "/{permission_id}",
    response_model=PermissionResponse,
    responses={
        404: {
            "description": "No se encontró ningún permiso de usuario",
        }
    },
)
def update_permission_endpoint(
    permission_id: int,
    permission_data: PermissionUpdate,
    db: Session = Depends(get_db),
):

    permission = update_permission(
        db=db,
        permission_id=permission_id,
        permission_data=permission_data,
    )

    if permission is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún permiso de usuario",
        )

    return permission


@router.delete(
    "/{permission_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ningún permiso de usuario",
        }
    },
)
def delete_permission_endpoint(
    permission_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_permission(
        db=db,
        permission_id=permission_id,
    )
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún permiso de usuario",
        )
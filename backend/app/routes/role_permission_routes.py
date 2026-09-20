from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.role_permission_schema import RolePermissionCreate, RolePermissionResponse
from app.services.role_permission_service import create_role_permission

from app.core.exceptions import RolePermissionAlreadyAssociatedError

router = APIRouter(
    prefix="/role-permission",
    tags=["Role Permission"]
)

@router.post(
    "/",
    response_model=RolePermissionResponse
)
def create_role_permission_endpoint(
    role_permission_data: RolePermissionCreate,
    db: Session = Depends(get_db),
):

    try:
        role_permission = create_role_permission(
            db=db,
            role_id=role_permission_data.role_id,
            permission_id=role_permission_data.permission_id,
        )
        
    except RolePermissionAlreadyAssociatedError:
            raise HTTPException(
                status_code=409,
                detail="El permiso ya está asociado al rol."
            )
            
    if role_permission is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el rol o el permiso indicado."
        )

    return role_permission

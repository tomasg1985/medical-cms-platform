from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_role_schema import UserRoleCreate, UserRoleResponse
from app.services.user_role_service import create_user_role

from app.core.exceptions import UserRoleAlreadyAssociatedError

router = APIRouter(
    prefix="/user-role",
    tags=["User Role"],
)

@router.post(
    "/",
    response_model=UserRoleResponse
)
def create_user_role_endpoint(
    user_role_data: UserRoleCreate,
    db: Session = Depends(get_db),
):
    
    try:
        user_role = create_user_role(
            db=db,
            user_id=user_role_data.user_id,
            role_id=user_role_data.role_id,
        )
        
    except UserRoleAlreadyAssociatedError:
            raise HTTPException(
                status_code=409,
                detail="El usuario ya está asociado a este rol."
            )
            
    if user_role is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el usuario o rol indicado."
        )

    return user_role
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_clinic_schema import UserClinicCreate, UserClinicResponse
from app.services.user_clinic_service import create_user_clinic

from app.core.exceptions import UserClinicAlreadyAssociatedError

router = APIRouter(
    prefix="/user-clinic",
    tags=["User Clinic"]
)

@router.post(
    "/",
    response_model=UserClinicResponse
)
def create_user_clinic_endpoint(
    user_clinic_data: UserClinicCreate,
    db: Session = Depends(get_db),
):

    try:
        user_clinic = create_user_clinic(
            db=db,
            user_id=user_clinic_data.user_id,
            clinic_id=user_clinic_data.clinic_id
        )
        
    except UserClinicAlreadyAssociatedError:
            raise HTTPException(
                status_code=409,
                detail="El usuario ya está asociado a esta clínica."
            )
            
    if user_clinic is None:
        raise HTTPException(
                    status_code=404,
                    detail="No se encontró una clínica o usuario válido para la asociación."
                )
    
    return user_clinic
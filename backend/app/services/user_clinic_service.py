from sqlalchemy.orm import Session

from app.models.user_clinic_model import UserClinic

from app.repositories.user_clinic_repository import UserClinicRepository
from app.repositories.user_repository import UserRepository
from app.repositories.clinic_repository import ClinicRepository

from app.core.exceptions import UserClinicAlreadyAssociatedError

user_clinic_repository = UserClinicRepository()
user_repository = UserRepository()
clinic_repository = ClinicRepository()


def create_user_clinic(
    db: Session,
    user_id: int,
    clinic_id: int
    ) -> UserClinic | None:
    
    
    user = user_repository.get_by_id(
        db=db,
        user_id=user_id
    )
    
    if user is None:
        return None
    
    clinic = clinic_repository.get_by_id(
        db=db,
        clinic_id=clinic_id
    )
    
    if clinic is None:
        return None

    existing = user_clinic_repository.get_by_user_and_clinic(
        db=db,
        user_id=user_id,
        clinic_id=clinic_id
    )

    if existing is not None:
        raise UserClinicAlreadyAssociatedError()

    user_clinic = UserClinic(
        user_id=user_id,
        clinic_id=clinic_id
    )

    user_clinic = user_clinic_repository.create(
        db=db,
        user_clinic=user_clinic
    )
    
    return user_clinic
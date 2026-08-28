from sqlalchemy.orm import Session

from app.models.clinic_model import Clinic
from app.repositories.clinic_repository import ClinicRepository

clinic_repository = ClinicRepository()


def create_clinic(
    db: Session,
    name: str
) -> Clinic:

    clinic = Clinic(
        name=name
    )

    clinic = clinic_repository.create(
            db=db,
            clinic=clinic
        )

    return clinic



def get_clinics(db: Session) -> list[Clinic]:

    clinics = clinic_repository.get_clinics(
        db=db
    )

    return clinics


def get_clinic(db: Session, clinic_id: int) -> Clinic | None:

    clinic = clinic_repository.get_by_id(
        db=db,
        clinic_id=clinic_id
    )

    return clinic


def update_clinic(db: Session, clinic_id: int, name: str) -> Clinic | None:

    clinic = get_clinic(
        db=db,
        clinic_id=clinic_id,
    )

    if clinic is None:
        return None

    clinic.name = name

    clinic = clinic_repository.update(
            db=db,
            clinic=clinic
        )

    return clinic



def delete_clinic(db: Session, clinic_id: int) -> bool:

    clinic = get_clinic(
        db=db,
        clinic_id=clinic_id,
    )

    if clinic is None:
        return False

    return clinic_repository.delete(
        db=db,
        clinic=clinic
    )
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.clinic import Clinic


def create_clinic(db: Session, name: str) -> Clinic:
    clinic = Clinic(
        name=name
    )

    try:
        db.add(clinic)
        db.commit()
        db.refresh(clinic)

        return clinic

    except Exception:
        db.rollback()
        raise


def get_clinics(db: Session) -> list[Clinic]:
    statement = select(Clinic)
    result = db.execute(statement)
    clinics = result.scalars().all()

    return clinics


def get_clinic(db: Session, clinic_id: int) -> Clinic | None:
    statement = select(Clinic).where(Clinic.id == clinic_id)
    result = db.execute(statement)
    clinic = result.scalar_one_or_none()

    return clinic


def update_clinic(db: Session, clinic_id: int, name: str) -> Clinic | None:

    clinic = get_clinic(
        db=db,
        clinic_id=clinic_id,
    )

    if clinic is None:
        return None

    clinic.name = name

    try:
        db.commit()
        db.refresh(clinic)

        return clinic

    except Exception:
        db.rollback()
        raise


def delete_clinic(db: Session, clinic_id: int) -> bool:

    clinic = get_clinic(
        db=db,
        clinic_id=clinic_id,
    )

    if clinic is None:
        return False

    try:
        db.delete(clinic)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise
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

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.clinic_model import Clinic


class ClinicRepository:
    def get_by_id(self, db: Session, clinic_id: int) -> Clinic | None:
        statement = select(Clinic).where(Clinic.id == clinic_id)
        result = db.execute(statement)
        clinic = result.scalar_one_or_none()

        return clinic


    def get_clinics(self, db: Session) -> list[Clinic]:
        statement = select(Clinic)
        result = db.execute(statement)
        clinics = result.scalars().all()

        return clinics


    def create(self, db: Session, clinic: Clinic) -> Clinic:

        try:
            db.add(clinic)
            db.commit()
            db.refresh(clinic)

            return clinic

        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, clinic: Clinic)-> Clinic:

        try:
            db.commit()
            db.refresh(clinic)

            return clinic

        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, clinic: Clinic) -> bool:
        
        try:
            db.delete(clinic)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
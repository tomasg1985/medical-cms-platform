from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.prescription_model import Prescription

class PrescriptionRepository:
    def get_by_id(self, db: Session, prescription_id: int) -> Prescription | None:
        statement = (
            select(Prescription)
            .where(Prescription.id == prescription_id)
        )
        result = db.execute(statement)
        prescription = result.scalar_one_or_none()
        
        return prescription


    def get_prescriptions(self, db: Session) -> list[Prescription]:
        statement = select(Prescription)
        result = db.execute(statement)
        prescriptions = result.scalars().all()
        
        return prescriptions


    def create(self, db: Session, prescription: Prescription) -> Prescription:
        try:
            db.add(prescription)
            db.commit()
            db.refresh(prescription)
            
            return prescription
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, prescription: Prescription) -> Prescription:
        try:
            db.commit()
            db.refresh(prescription)

            return prescription
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, prescription: Prescription) -> bool:
        try:
            db.delete(prescription)
            db.commit()

            return True

        except Exception:
            db.rollback()
            raise
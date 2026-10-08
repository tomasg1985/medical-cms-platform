from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.medication_model import Medication

class MedicationRepository:
    def get_by_id(self, db: Session, medication_id: int) -> Medication | None:
        statement = (
            select(Medication)
            .where(Medication.id == medication_id)
        )
        result = db.execute(statement)
        medication = result.scalar_one_or_none()

        return medication


    def get_medications(self, db: Session) -> list[Medication]:
        statement = select(Medication)
        result = db.execute(statement)
        medications = result.scalars().all()

        return medications


    def create(self, db: Session, medication: Medication) -> Medication:
        try:
            db.add(medication)
            db.commit()
            db.refresh(medication)
            
            return medication
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, medication: Medication) -> Medication:
        try:
            db.commit()
            db.refresh(medication)

            return medication
        except Exception:
            db.rollback()
            raise
        

    def delete(self, db: Session, medication: Medication) -> bool:
        try:
            db.delete(medication)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
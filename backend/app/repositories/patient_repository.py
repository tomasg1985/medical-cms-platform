from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.patient_model import Patient

class PatientRepository:
    def get_by_id(self, db: Session, patient_id: int) -> Patient | None:
        statement = select(Patient).options(joinedload(Patient.clinic)).where(Patient.id == patient_id)
        result = db.execute(statement)
        patient = result.scalar_one_or_none()
        
        return patient


    def get_patients(self, db: Session, clinic_id: int | None = None) -> list[Patient]:
        statement = select(Patient).options(joinedload(Patient.clinic))
        
        if clinic_id is not None:
            statement = statement.where(
                Patient.clinic_id == clinic_id
            )

        result = db.execute(statement)
        patients = result.scalars().all()
        
        return patients


    def create(self, db: Session, patient: Patient) -> Patient:
        
        try:
            db.add(patient)
            db.commit()
            db.refresh(patient)

            return patient

        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, patient: Patient) -> Patient:

        try:
            db.commit()
            db.refresh(patient)

            return patient
    
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, patient: Patient) -> bool:

        try:
            db.delete(patient)
            db.commit()

            return True

        except Exception:
            db.rollback()
            raise
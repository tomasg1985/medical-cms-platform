from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.patient_clinics_model import PatientClinic


class PatientClinicRepository:

    def create(self, db: Session, patient_clinic: PatientClinic) -> PatientClinic:
            
        try:
            db.add(patient_clinic)
            db.commit()
            db.refresh(patient_clinic)

            return patient_clinic

        except Exception:
            db.rollback()
            raise


    def get_by_patient_and_clinic(self, db: Session, patient_id: int, clinic_id: int) -> PatientClinic | None:
        statement = select(PatientClinic).where(PatientClinic.patient_id == patient_id, PatientClinic.clinic_id == clinic_id)
        result = db.execute(statement)
        patient_clinic = result.scalar_one_or_none()
        
        return patient_clinic
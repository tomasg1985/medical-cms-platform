from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.medical_record_model import MedicalRecord

class MedicalRecordRepository:
    def get_by_id(self, db: Session, medical_record_id: int) -> MedicalRecord | None:
        statement = (
            select(MedicalRecord)
            .where(MedicalRecord.id == medical_record_id)
        )
        result = db.execute(statement)
        medical_record = result.scalar_one_or_none()
        
        return medical_record


    def get_medical_records(self, db: Session) -> list[MedicalRecord]:
        statement = select(MedicalRecord)
        result = db.execute(statement)
        medical_records = result.scalars().all()
        
        return medical_records


    def get_patient_clinic(
        self,
        db: Session,
        patient_id: int,
        clinic_id: int
    ) -> MedicalRecord | None:
        
        statement = select(MedicalRecord).where(
            MedicalRecord.patient_id == patient_id,
            MedicalRecord.clinic_id == clinic_id
        )
        result = db.execute(statement)
        patient_clinic = result.scalar_one_or_none()
        
        return patient_clinic


    def create(self, db: Session, medical_record: MedicalRecord) -> MedicalRecord:
        try:
            db.add(medical_record)
            db.commit()
            db.refresh(medical_record)
            
            return medical_record
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, medical_record: MedicalRecord) -> MedicalRecord:
        try:
            db.commit()
            db.refresh(medical_record)

            return medical_record
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, medical_record: MedicalRecord) -> bool:
        try:
            db.delete(medical_record)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
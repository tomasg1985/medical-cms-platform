from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.patient_contacts_model import PatientContact

class PatientContactRepository:
    def get_by_id(self, db: Session, patient_contacts_id: int) -> PatientContact | None:
        statement = (
            select(PatientContact)
            .where(PatientContact.id == patient_contacts_id)
        )
        result = db.execute(statement)
        patient_contacts = result.scalar_one_or_none()
        
        return patient_contacts


    def get_patient_contacts(self, db: Session) -> list[PatientContact]:
        statement = select(PatientContact)
        result = db.execute(statement)
        patients_contacts = result.scalars().all()
        
        return patients_contacts


    def create(self, db: Session, patient_contacts: PatientContact) -> PatientContact:
        try:
            db.add(patient_contacts)
            db.commit()
            db.refresh(patient_contacts)
            
            return patient_contacts
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, patient_contacts: PatientContact) -> PatientContact:
        try:
            db.commit()
            db.refresh(patient_contacts)

            return patient_contacts
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, patient_contacts: PatientContact) -> bool:
            try:
                db.delete(patient_contacts)
                db.commit()
                
                return True
            
            except Exception:
                db.rollback()
                raise
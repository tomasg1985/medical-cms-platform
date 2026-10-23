from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.patient_contacts_model import PatientContact


class PatientContactRepository:
    def get_by_id(
        self,
        db: Session,
        patient_contact_id: int,
    ) -> PatientContact | None:
        statement = select(PatientContact).where(
            PatientContact.id == patient_contact_id
        )
        result = db.execute(statement)
        return result.scalar_one_or_none()

    def get_patient_contacts(self, db: Session) -> list[PatientContact]:
        statement = select(PatientContact)
        result = db.execute(statement)
        return result.scalars().all()

    def create(
        self,
        db: Session,
        patient_contact: PatientContact,
    ) -> PatientContact:
        try:
            db.add(patient_contact)
            db.commit()
            db.refresh(patient_contact)
            return patient_contact
        except Exception:
            db.rollback()
            raise

    def update(
        self,
        db: Session,
        patient_contact: PatientContact,
    ) -> PatientContact:
        try:
            db.commit()
            db.refresh(patient_contact)
            return patient_contact
        except Exception:
            db.rollback()
            raise

    def delete(
        self,
        db: Session,
        patient_contact: PatientContact,
    ) -> bool:
        try:
            db.delete(patient_contact)
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise

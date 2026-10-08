from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.medical_document_model import MedicalDocument

class MedicalDocumentRepository:
    def get_by_id(self, db: Session, medical_document_id: int) -> MedicalDocument | None:
        statement = (
            select(MedicalDocument)
            .where(MedicalDocument.id == medical_document_id)
        )
        result = db.execute(statement)
        medical_document = result.scalar_one_or_none()
        
        return medical_document


    def get_medical_documents(self, db: Session) -> list[MedicalDocument]:
        statement = select(MedicalDocument)
        result = db.execute(statement)
        medical_documents = result.scalars().all()
        
        return medical_documents


    def get_by_patient_professional_clinic_medical_record(
        self,
        db: Session,
        patient_id: int,
        professional_id: int,
        clinic_id: int,
        medical_record_id: int
    ) -> MedicalDocument | None:
        
        statement = select(MedicalDocument).where(
            MedicalDocument.patient_id == patient_id,
            MedicalDocument.professional_id == professional_id,
            MedicalDocument.clinic_id == clinic_id,
            MedicalDocument.medical_record_id == medical_record_id,
        )
        result = db.execute(statement)
        patient_professional_clinic_medical_record = result.scalar_one_or_none()
        
        return patient_professional_clinic_medical_record


    def create(self, db: Session, medical_document: MedicalDocument) -> MedicalDocument:
        try:
            db.add(medical_document)
            db.commit()
            db.refresh(medical_document)
            
            return medical_document
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, medical_document: MedicalDocument) -> MedicalDocument:
        try:
            db.commit()
            db.refresh(medical_document)

            return medical_document
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, medical_document: MedicalDocument) -> bool:
        try:
            db.delete(medical_document)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
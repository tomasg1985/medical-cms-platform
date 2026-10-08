from sqlalchemy.orm import Session

from app.models.medical_document_model import MedicalDocument

from app.repositories.medical_document_repository import MedicalDocumentRepository
from app.repositories.patient_repository import PatientRepository
from app.repositories.professional_repository import ProfessionalRepository
from app.repositories.clinic_repository import ClinicRepository
from app.repositories.medical_record_repository import MedicalRecordRepository

from app.schemas.medical_document_schema import MedicalDocumentCreate, MedicalDocumentUpdate
from app.core.exceptions import ClinicNotFoundError, MedicalDocumentAlreadyExistsException, MedicalDocumentNotFoundException, MedicalRecordNotFoundException, PatientNotFoundError, ProfessionalNotFoundError

medical_document_repository = MedicalDocumentRepository()
patient_repository = PatientRepository()
professional_repository = ProfessionalRepository()
clinic_repository = ClinicRepository()
medical_record_repository = MedicalRecordRepository()

def create_medical_document(
    db: Session,
    medical_document_data: MedicalDocumentCreate,
) -> MedicalDocument:
    patient_id = medical_document_data.patient_id
    professional_id = medical_document_data.professional_id
    clinic_id = medical_document_data.clinic_id
    medical_record_id = medical_document_data.medical_record_id

    patient = patient_repository.get_by_id(
        db=db,
        patient_id=patient_id
    )
    
    if patient is None:
        raise PatientNotFoundError()
    
    
    professional = professional_repository.get_by_id(
        db=db,
        professional_id=professional_id
    )
    
    if professional is None:
        raise ProfessionalNotFoundError()
    
    clinic = clinic_repository.get_by_id(
        db=db,
        clinic_id=clinic_id
    )
    
    if clinic is None:
        raise ClinicNotFoundError()
    
    medical_record = medical_record_repository.get_by_id(
        db=db,
        medical_record_id=medical_record_id
    )
    
    if medical_record is None:
        raise MedicalRecordNotFoundException()
    
    existing = medical_document_repository.get_by_patient_professional_clinic_medical_record(
        db=db,
        patient_id=patient_id,
        professional_id=professional_id,
        clinic_id=clinic_id,
        medical_record_id=medical_record_id
    )
    
    if existing is not None:
        raise MedicalDocumentAlreadyExistsException()
    
    medical_document = MedicalDocument(
        name=medical_document_data.name,
        file_path=medical_document_data.file_path,
        document_type=medical_document_data.document_type,
        patient_id=patient_id,
        professional_id=professional_id,
        clinic_id=clinic_id,
        medical_record_id=medical_record_id
    )
    
    medical_document = medical_document_repository.create(
        db=db,
        medical_document=medical_document
    )

    return medical_document

def get_medical_documents(
    db: Session
) -> list[MedicalDocument]:
    
    medical_documents = medical_document_repository.get_medical_documents(
        db=db
    )
    
    return medical_documents


def get_medical_document(
    db: Session,
    medical_document_id: int
) -> MedicalDocument:
    
    medical_document = medical_document_repository.get_by_id(
        db=db,
        medical_document_id=medical_document_id
    )
    
    if medical_document is None:
        raise MedicalDocumentNotFoundException()

    return medical_document


def update_medical_document(
    db: Session,
    medical_document_id: int,
    medical_document_data: MedicalDocumentUpdate
) -> MedicalDocument | None:
    
    medical_document = get_medical_document(
        db=db,
        medical_document_id=medical_document_id
    )
    
    medical_document.name = medical_document_data.name
    medical_document.file_path = medical_document_data.file_path
    medical_document.document_type = medical_document_data.document_type
    
    medical_document = medical_document_repository.update(
        db=db,
        medical_document=medical_document
    )
    
    return medical_document


def delete_medical_document(
    db: Session,
    medical_document_id: int
) -> bool:
    
    medical_document = get_medical_document(
        db=db,
        medical_document_id=medical_document_id
    )
    
    return medical_document_repository.delete(
        db=db,
        medical_document=medical_document
    )
from sqlalchemy.orm import Session

from app.models.study_model import Study
from app.models.patient_model import Patient
from app.models.professional_model import Professional
from app.models.medical_record_model import MedicalRecord
from app.models.appointment_model import Appointment

from app.schemas.study_schema import StudyUpdate, StudyCreate

from app.repositories.study_repository import StudyRepository

study_repository = StudyRepository()

def create_study(
    db: Session,
    patient_id: int,
    professional_id: int,
    medical_record_id: int,
    appointment_id: int,
    study_data: StudyCreate
) -> Study | None:

    patient = db.get(Patient, patient_id)
    if patient is None:
        return None

    professional = db.get(Professional, professional_id)
    if professional is None:
        return None

    medical_record = db.get(MedicalRecord, medical_record_id)
    if medical_record is None:
        return None
    
    appointment = db.get(Appointment, appointment_id)
    if appointment is None:
        return None

    study = Study(
        study_type=study_data.study_type,
        file_path=study_data.file_path,
        status=study_data.status,
        requested_at=study_data.requested_at,
        completed_at=study_data.completed_at,
        patient_id=patient_id,
        professional_id=professional_id,
        medical_record_id=medical_record_id,
        appointment_id=appointment_id
    )
    
    study = study_repository.create(
        db=db,
        study=study
    )
    
    return study


def get_studies(
    db: Session
) -> list[Study]:
    
    studies = study_repository.get_studies(
        db=db
    )
    
    return studies


def get_study(
    db: Session,
    study_id: int
) -> Study | None:
    
    study = study_repository.get_by_id(
        db=db,
        study_id=study_id
    )
    
    return study


def update_study(
    db: Session,
    study_id: int,
    study_data: StudyUpdate 
) -> Study | None:
    
    study = get_study(
        db=db,
        study_id=study_id
    )
    
    if study is None:
        return None
    
    data = study_data.model_dump(
        exclude_unset=True
    )
    
    for field, value in data.items():
        setattr(study, field, value)
        
    study = study_repository.update(
        db=db,
        study=study
    )
    
    return study


def delete_study(
    db: Session,
    study_id: int
) -> bool:
    
    study = get_study(
        db=db,
        study_id=study_id
    )
    
    if study is None:
        return False
    
    return study_repository.delete(
        db=db,
        study=study
    )
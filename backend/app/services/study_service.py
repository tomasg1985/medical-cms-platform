from sqlalchemy.orm import Session

from app.core.exceptions import AppointmentNotFoundError, MedicalRecordNotFoundException, PatientNotFoundError, ProfessionalNotFoundError, StudyNotFoundException
from app.models.appointment_model import Appointment
from app.models.medical_record_model import MedicalRecord
from app.models.patient_model import Patient
from app.models.professional_model import Professional
from app.models.study_model import Study
from app.repositories.study_repository import StudyRepository
from app.schemas.study_schema import StudyCreate, StudyUpdate

study_repository = StudyRepository()


def create_study(db: Session, study_data: StudyCreate) -> Study:
    patient = db.get(Patient, study_data.patient_id)
    if patient is None:
        raise PatientNotFoundError()

    professional = db.get(Professional, study_data.professional_id)
    if professional is None:
        raise ProfessionalNotFoundError()

    medical_record = db.get(MedicalRecord, study_data.medical_record_id)
    if medical_record is None:
        raise MedicalRecordNotFoundException()

    appointment = db.get(Appointment, study_data.appointment_id)
    if appointment is None:
        raise AppointmentNotFoundError()

    study = Study(
        study_type=study_data.study_type,
        file_path=study_data.file_path,
        status=study_data.status,
        requested_at=study_data.requested_at,
        completed_at=study_data.completed_at,
        patient_id=study_data.patient_id,
        professional_id=study_data.professional_id,
        medical_record_id=study_data.medical_record_id,
        appointment_id=study_data.appointment_id,
    )

    return study_repository.create(
        db=db,
        study=study,
    )


def get_studies(db: Session) -> list[Study]:
    return study_repository.get_studies(db=db)


def get_study(db: Session, study_id: int) -> Study:
    study = study_repository.get_by_id(
        db=db,
        study_id=study_id,
    )
    if study is None:
        raise StudyNotFoundException()

    return study


def update_study(
    db: Session,
    study_id: int,
    study_data: StudyUpdate,
) -> Study:
    study = get_study(
        db=db,
        study_id=study_id,
    )

    for field, value in study_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    ).items():
        setattr(study, field, value)

    return study_repository.update(
        db=db,
        study=study,
    )


def delete_study(db: Session, study_id: int) -> bool:
    study = get_study(
        db=db,
        study_id=study_id,
    )

    return study_repository.delete(
        db=db,
        study=study,
    )

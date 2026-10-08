from sqlalchemy.orm import Session

from app.models.prescription_model import Prescription
from app.models.patient_model import Patient
from app.models.professional_model import Professional
from app.models.medical_record_model import MedicalRecord
from app.models.appointment_model import Appointment

from app.schemas.prescription_schema import PrescriptionUpdate, PrescriptionCreate

from app.repositories.prescription_repository import PrescriptionRepository

from app.core.exceptions import PrescriptionNotFoundException, PatientNotFoundError, ProfessionalNotFoundError, MedicalRecordNotFoundException, AppointmentNotFoundError

prescription_repository = PrescriptionRepository()

def create_prescription(
    db: Session,
    patient_id: int,
    professional_id: int,
    medical_record_id: int,
    appointment_id: int,
    prescription_data: PrescriptionCreate
) -> Prescription | None:
    
    patient = db.get(Patient, patient_id)
    if patient is None:
        raise PatientNotFoundError()
    
    professional = db.get(Professional, professional_id)
    if professional is None:
        raise ProfessionalNotFoundError()
    
    medical_record = db.get(MedicalRecord, medical_record_id)
    if medical_record is None:
        raise MedicalRecordNotFoundException()
    
    appointment = db.get(Appointment, appointment_id)
    if appointment is None:
        raise AppointmentNotFoundError()
    
    prescription = Prescription(
        prescription_date=prescription_data.prescription_date,
        instructions=prescription_data.instructions,
        status=prescription_data.status,
        patient_id=patient_id,
        professional_id=professional_id,
        medical_record_id=medical_record_id,
        appointment_id=appointment_id
    )
    
    prescription = prescription_repository.create(
        db=db,
        prescription=prescription
    )
    
    return prescription


def prescriptions(
    db: Session
) -> list[Prescription]:
    
    prescriptions = prescription_repository.get_prescriptions(
        db=db
    )
    
    return prescriptions


def get_prescription(
    db: Session,
    prescription_id: int
) -> Prescription | None:
    
    
    prescription = prescription_repository.get_by_id(
        db=db,
        prescription_id=prescription_id
    )
    
    return prescription


def update_prescription(
    db: Session,
    prescription_id: int,
    prescription_data: PrescriptionUpdate
) -> Prescription | None:
    
    prescription = get_prescription(
        db=db,
        prescription_id=prescription_id
    )
    
    if prescription is None:
        raise PrescriptionNotFoundException()
    
    data = prescription_data.model_dump(
        exclude_unset=True
    )
    
    for field, value in data.items():
        setattr(prescription,field, value)
        
    prescription = prescription_repository.update(
        db=db,
        prescription=prescription
    )
    
    return prescription


def delete_prescription(
    db: Session,
    prescription_id: int
) -> bool:
    
    prescription = get_prescription(
        db=db,
        prescription_id=prescription_id
    )
    
    if prescription is None:
        raise PrescriptionNotFoundException()
    
    return prescription_repository.delete(
        db=db,
        prescription=prescription
    )
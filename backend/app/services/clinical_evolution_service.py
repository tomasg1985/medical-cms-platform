from sqlalchemy.orm import Session

from app.models.clinical_evolution_model import ClinicalEvolution

from app.repositories.clinical_evolution_repository import ClinicalEvolutionRerpository
from app.repositories.medical_record_repository import MedicalRecordRepository
from app.repositories.professional_repository import ProfessionalRepository
from app.repositories.appointment_repository import AppointmentRepository

clinical_evolution_repository = ClinicalEvolutionRerpository()
medical_record_repository = MedicalRecordRepository()
professional_repository = ProfessionalRepository()
appointment_repository = AppointmentRepository()


def create_clinical_evolution(
    db: Session,
    content: str,
    medical_record_id: int,
    professional_id: int,
    appointment_id: int
) -> ClinicalEvolution | None:

    medical_record = medical_record_repository.get_by_id(
        db=db,
        medical_record_id=medical_record_id
    )
    
    if medical_record is None:
        return None
    
    professional = professional_repository.get_by_id(
        db=db,
        professional_id=professional_id
    )
    
    if professional is None:
        return None
    
    appointment = appointment_repository.get_by_id(
        db=db,
        appointment_id=appointment_id
    )
    
    if appointment is None:
        return None
    
    existing = clinical_evolution_repository.get_by_medical_professional_appointment(
        db=db,
        medical_record_id=medical_record_id,
        professional_id=professional_id,
        appointment_id=appointment_id
    )
    
    if existing is not None:
        return None
    
    clinical_evolution = ClinicalEvolution(
        content=content,
        medical_record_id=medical_record_id,
        professional_id=professional_id,
        appointment_id=appointment_id
    )
    
    clinical_evolution = clinical_evolution_repository.create(
        db=db,
        clinical_evolution=clinical_evolution
    )
    
    return clinical_evolution
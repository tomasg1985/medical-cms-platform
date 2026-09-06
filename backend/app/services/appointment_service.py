from sqlalchemy.orm import Session

from app.models.appointment_model import Appointment
from app.models.patient_model import Patient
from app.models.professional_model import Professional
from app.models.clinic_model import Clinic
from app.models.specialty_model import Specialty
from app.models.schedule_availability_model import ScheduleAvailability

from app.schemas.appointment_schema import AppointmentCreate, AppointmentUpdate

from app.repositories.appointment_repository import AppointmentRepository

appointment_repository = AppointmentRepository()

def create(
    db: Session,
    appointment_data: AppointmentCreate
) -> Appointment:

    availability = db.get(ScheduleAvailability, appointment_data.schedule_availability_id)

    if availability is None:
        return None

    if availability.professional != professional:
        return None
    
    if availability.clinic != clinic:
        return None
    
    if availability.specialty != specialty:
        return None

    patient = db.get(Patient, appointment_data.patient_id)

    if patient is None:
        return None

    professional = db.get(Professional, appointment_data.professional_id)

    if professional is None:
        return None

    clinic = db.get(Clinic, appointment_data.clinic_id)

    if clinic is None:
        return None

    if not clinic in professional.clinics:
        return None
    

    if not specialty in clinic.specialties:
        return None

    specialty = db.get(Specialty, appointment_data.specialty_id)

    if specialty is None:
        return None

    if not specialty in professional.specialties:
        return None
    
    if appointment_data.appointment_date < availability.valid_from:
        return None

    appointment = Appointment(
        reservation_code=appointment_data.reservation_code,
        appointment_date=appointment_data.appointment_date,
        appointment_hour=appointment_data.appointment_hour,
        consulting_duration=availability.consulting_duration,
        consulting_mode=appointment_data.consulting_mode,
        appointment_state=appointment_data.appointment_state,
        consulting_reason=appointment_data.consulting_reason,
        cancelation_reason=appointment_data.cancelation_reason,
        amount_paid=appointment_data.amount_paid,
        payment_status=appointment_data.payment_status,
        schedule_availability_id=appointment_data.schedule_availability_id,
        clinic_id=appointment_data.clinic_id,
        patient_id=appointment_data.patient_id,
        professional_id=appointment_data.professional_id,
        specialty_id=appointment_data.specialty_id,
    )

    appointment = appointment_repository.create(
        db=db,
        appointment=appointment
    )
    
    return appointment


def get_appointments(db: Session) -> list[Appointment]:
    appointments = appointment_repository.get_appointments(
        db=db
    )
    
    return appointments


def get_appointment(
    db: Session,
    appointment_id: int
) -> Appointment | None:

    appointment = appointment_repository.get_by_id(
        db=db,
        appointment_id=appointment_id
    )

    return appointment


def update_appointment(
    db: Session,
    appointment_id: int,
    appointment_data: AppointmentUpdate
) -> Appointment | None:

    appointment = get_appointment(
        db=db,
        appointment_id=appointment_id,
    )

    if appointment is None:
        return None
    
    data = appointment_data.model_dump(exclude_unset=True)
    
    for field, value in data.items():
        setattr(appointment, field, value)

    appointment = appointment_repository.update(
        db=db,
        appointment=appointment
    )

    return appointment


def delete(
    db: Session,
    appointment_id: int
) -> bool:
    
    appointment = get_appointment(
        db=db,
        appointment_id=appointment_id,
    )
    
    if appointment is None:
        return False
    
    return appointment_repository.delete(
        db=db,
        appointment=appointment
    )
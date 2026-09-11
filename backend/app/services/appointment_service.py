from datetime import datetime, timedelta

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.appointment_model import Appointment
from app.models.patient_model import Patient
from app.models.professional_model import Professional
from app.models.clinic_model import Clinic
from app.models.specialty_model import Specialty
from app.models.schedule_availability_model import ScheduleAvailability

from app.schemas.appointment_schema import AppointmentCreate, AppointmentUpdate

from app.repositories.appointment_repository import AppointmentRepository

from app.core.exceptions import PatientNotFoundError, ProfessionalNotFoundError, ClinicNotFoundError, SpecialtyNotFoundError, AppointmentAvailabilityError, AppointmentConflictError, AppointmentNotFoundError, AppointmentCancelledError

appointment_repository = AppointmentRepository()

def create_appointment(
    db: Session,
    appointment_data: AppointmentCreate
) -> Appointment:

    # Obtener y verificar paciente
    patient = db.get(Patient, appointment_data.patient_id)
    if patient is None:
        raise PatientNotFoundError

    # Obtener y verificar profesional
    professional = db.get(Professional, appointment_data.professional_id)
    if professional is None:
        raise ProfessionalNotFoundError

    # Obtener y verificar clinica
    clinic = db.get(Clinic, appointment_data.clinic_id)
    if clinic is None:
        raise ClinicNotFoundError

    # Obtener y verificar especialidad
    specialty = db.get(Specialty, appointment_data.specialty_id)
    if specialty is None:
        raise SpecialtyNotFoundError

    # RELACIÓN ENTRE ENTIDADES

    # Verificar professional con clinica
    if not clinic in professional.clinics:
        raise AppointmentAvailabilityError

    # Verificar profesional con especialidad
    if not specialty in professional.specialties:
        raise AppointmentAvailabilityError

    # Verificar clinica con especialidad
    if not specialty in clinic.specialties:
        raise AppointmentAvailabilityError
    
    # Obtener y verificar disponibilidad
    statement = (
        select(ScheduleAvailability)
        .where(
            ScheduleAvailability.professional_id == appointment_data.professional_id,
            ScheduleAvailability.clinic_id == appointment_data.clinic_id,
            ScheduleAvailability.specialty_id == appointment_data.specialty_id,
            ScheduleAvailability.weekday == appointment_data.appointment_date.weekday() + 1,
            ScheduleAvailability.valid_from <= appointment_data.appointment_date,
            ScheduleAvailability.start_hour <= appointment_data.appointment_hour,
            ScheduleAvailability.activity_status == "active",
            appointment_data.appointment_hour < ScheduleAvailability.end_hour,
            or_(
                ScheduleAvailability.valid_until.is_(None),
                ScheduleAvailability.valid_until >= appointment_data.appointment_date
                
            )
        )
    )
    
    result = db.execute(statement)
    availability = result.scalar_one_or_none()
    
    if availability is None:
        raise AppointmentAvailabilityError

    appointment_start = datetime.combine(appointment_data.appointment_date, appointment_data.appointment_hour)
    appointment_end = appointment_start + timedelta(minutes=availability.consulting_duration)

    availability_end = datetime.combine(appointment_data.appointment_date, availability.end_hour)

    if appointment_end > availability_end:
        raise AppointmentAvailabilityError

    appointments = appointment_repository.get_appointments_by_professional_and_date(
        db=db,
        professional_id=appointment_data.professional_id,
        appointment_date=appointment_data.appointment_date
    )

    for existing_appointment in appointments:
        existing_start = datetime.combine(existing_appointment.appointment_date, existing_appointment.appointment_hour)
        existing_end = existing_start + timedelta(minutes=existing_appointment.consulting_duration)

        if appointment_start < existing_end and appointment_end > existing_start:
            raise AppointmentConflictError

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
        schedule_availability_id=availability.id,
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
) -> Appointment:

    appointment = get_appointment(
        db=db,
        appointment_id=appointment_id,
    )

    if appointment is None:
        raise AppointmentNotFoundError
    
    if appointment.appointment_state == "cancelled":
        raise AppointmentCancelledError

    data = appointment_data.model_dump(exclude_unset=True)

    new_date = data.get(
        "appointment_date",
        appointment.appointment_date
    )

    new_hour = data.get(
        "appointment_hour",
        appointment.appointment_hour
    )

    date_or_hour_changed = (
        "appointment_date" in data
        or "appointment_hour" in data
    )
    
    if date_or_hour_changed:

        statement = (
            select(ScheduleAvailability)
            .where(
                ScheduleAvailability.professional_id == appointment.professional_id,
                ScheduleAvailability.clinic_id == appointment.clinic_id,
                ScheduleAvailability.specialty_id == appointment.specialty_id,
                ScheduleAvailability.weekday == new_date.weekday() + 1,
                ScheduleAvailability.valid_from <= new_date,
                ScheduleAvailability.start_hour <= new_hour,
                ScheduleAvailability.activity_status == "active",
                new_hour < ScheduleAvailability.end_hour,
                or_(
                    ScheduleAvailability.valid_until.is_(None),
                    ScheduleAvailability.valid_until >= new_date,
                )
            )
        )

        result = db.execute(statement)
        availability = result.scalar_one_or_none()

    else:
        availability = appointment.schedule_availability

    if availability is None:
        raise AppointmentAvailabilityError

    appointment_start = datetime.combine(
        new_date,
        new_hour
    )

    appointment_end = appointment_start + timedelta(
        minutes=availability.consulting_duration
    )

    availability_end = datetime.combine(
        new_date,
        availability.end_hour
    )

    if appointment_end > availability_end:
        raise AppointmentAvailabilityError

    appointments = appointment_repository.get_appointments_by_professional_and_date(
        db=db,
        professional_id=appointment.professional_id,
        appointment_date=new_date
    )

    for existing_appointment in appointments:

        if existing_appointment.id == appointment.id:
            continue

        existing_start = datetime.combine(
            existing_appointment.appointment_date,
            existing_appointment.appointment_hour
        )

        existing_end = existing_start + timedelta(
            minutes=existing_appointment.consulting_duration
        )

        if (
            appointment_start < existing_end
            and appointment_end > existing_start
        ):
            raise AppointmentConflictError

    for field, value in data.items():
        setattr(appointment, field, value)

    if date_or_hour_changed:
        appointment.schedule_availability_id = availability.id
        appointment.consulting_duration = availability.consulting_duration

    appointment = appointment_repository.update(
        db=db,
        appointment=appointment
    )

    return appointment


def delete_appointment(
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
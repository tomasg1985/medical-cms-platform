from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.appointment_model import Appointment

class AppointmentRepository:
    def get_by_id(self, db: Session, appointment_id: int) -> Appointment | None:
        statement = (
            select(Appointment)
            .options(
                selectinload(Appointment.patient),
                selectinload(Appointment.professional),
                selectinload(Appointment.clinic),
                selectinload(Appointment.specialty),
                selectinload(Appointment.schedule_availability)
            )
            .where(Appointment.id == appointment_id)
            )
        result = db.execute(statement)
        appointment = result.scalar_one_or_none()
        
        return appointment


    def get_appointments(self, db: Session) -> list[Appointment]:
        statement = (
            select(Appointment)
            .options(
                selectinload(Appointment.patient),
                selectinload(Appointment.professional),
                selectinload(Appointment.clinic),
                selectinload(Appointment.specialty)
            )
        )
        result = db.execute(statement)
        appointment = result.scalars().all()
        
        return appointment


    def create(self, db: Session, appointment: Appointment) -> Appointment:

        try:
            db.add(appointment)
            db.commit()
            db.refresh(appointment)
            
            return appointment

        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, appointment: Appointment) -> Appointment:
        
        try:
            db.commit()
            db.refresh(appointment)

            return appointment

        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, appointment: Appointment) -> bool:
        
        try:
            db.delete(appointment)
            db.commit()

            return True

        except Exception:
            db.rollback()
            raise


    def get_appointments_by_professional_and_date(
        self,
        db: Session,
        professional_id: int,
        appointment_date: date
    ) -> list[Appointment]:
        
        statement = (
            select(Appointment)
            .where(
                Appointment.professional_id == professional_id, 
                Appointment.appointment_date == appointment_date,
                Appointment.appointment_state != "cancelled"
            )
        )
        result = db.execute(statement)
        professional_appointments = result.scalars().all()
        
        return professional_appointments
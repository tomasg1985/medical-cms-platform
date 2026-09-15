from datetime import date, time
from decimal import Decimal

from typing import Optional

from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    reservation_code: str
    appointment_date: date
    appointment_hour: time
    consulting_mode: str
    consulting_duration: int
    appointment_state: str
    consulting_reason: str
    cancelation_reason: Optional[str] = None
    amount_paid: Decimal = 0
    payment_status: str

    clinic_id: int
    patient_id: int
    professional_id: int
    specialty_id: int
    schedule_availability_id: int


class AppointmentUpdate(BaseModel):
    reservation_code: Optional[str] = None
    appointment_date: Optional[date] = None
    appointment_hour: Optional[time] = None
    consulting_mode: Optional[str] = None
    consulting_duration: int
    appointment_state: Optional[str] = None
    consulting_reason: Optional[str] = None
    cancelation_reason: Optional[str] = None
    amount_paid: Optional[Decimal] = None
    payment_status: Optional[str] = None
    
    schedule_availability_id: int

class AppointmentResponse(BaseModel):
    id: int
    reservation_code: str
    appointment_date: date
    appointment_hour: time
    consulting_duration: int
    consulting_mode: str
    appointment_state: str
    consulting_reason: str
    cancelation_reason: Optional[str] = None
    amount_paid: Decimal
    payment_status: str
    
    clinic_id: int
    patient_id: int
    professional_id: int
    specialty_id: int
    schedule_availability_id: int
    
    model_config = {
        "from_attributes": True
    }
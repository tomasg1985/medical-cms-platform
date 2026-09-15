from pydantic import BaseModel
from typing import Optional

from datetime import date, time

class ScheduleAvailabilityCreate(BaseModel):
    weekday: int
    start_hour: time
    end_hour: time
    consulting_duration: int
    valid_from: date
    activity_status: str
    
    professional_id: int
    clinic_id: int
    specialty_id: int

class ScheduleAvailabilityUpdate(BaseModel):
    weekday: Optional[int] = None
    start_hour: Optional[time] = None
    end_hour: Optional[time] = None
    consulting_duration: Optional[int] = None
    valid_from: Optional[date] = None
    valid_until: Optional[date] = None
    activity_status: Optional[str] = None

class ScheduleAvailabilityResponse(BaseModel):
    id: int
    weekday: int
    start_hour: time
    end_hour: time
    consulting_duration: int
    valid_from: date
    valid_until: Optional[date] = None
    activity_status: str
    
    professional_id: int
    clinic_id: int
    specialty_id: int
        
    model_config = {
                "from_attributes": True
            }
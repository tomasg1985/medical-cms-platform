from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.appointment_schema import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from app.services.appointment_service import create_appointment, get_appointment, get_appointments, update_appointment,delete_appointment

from app.core.exceptions import PatientNotFoundError, ProfessionalNotFoundError, ClinicNotFoundError, SpecialtyNotFoundError, AppointmentAvailabilityError, AppointmentConflictError, AppointmentNotFoundError, AppointmentCancelledError

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.post("/", response_model=AppointmentResponse)
def create_appointment_endpoint(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
):
    try:
        appointment = create_appointment(
            db=db,
            appointment_data=appointment_data,
        )

        return appointment
    except PatientNotFoundError:
        raise HTTPException(
        status_code=404,
        detail="No se encontró el paciente solicitado",
    )

    except ProfessionalNotFoundError:
        raise HTTPException(
        status_code=404,
        detail="No se encontró el profesional médico solicitado",
    )

    except ClinicNotFoundError:
        raise HTTPException(
        status_code=404,
        detail="No se encontró la clínica solicitada",
    )

    except SpecialtyNotFoundError:
        raise HTTPException(
        status_code=404,
        detail="No se encontró la especialidad solicitada",
    )

    except AppointmentAvailabilityError:
        raise HTTPException(
        status_code=400,
        detail="No se encontró la disponibilidad u horario solicitado",
    )

    except AppointmentConflictError:
        raise HTTPException(
        status_code=409,
        detail="Se encontró una duplicidad en el horario o fecha solicitada",
    )


@router.get(
    "/",
    response_model=list[AppointmentResponse]
)
def get_appointments_endpoint(
    db: Session = Depends(get_db),
):
    appointments = get_appointments(db)

    return appointments


@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse,
    responses={
        404: {
            "description": "No se encontró ningún turno"
        }
    },
)
def get_appointment_endpoint(
    appointment_id: int,
    db: Session =  Depends(get_db),
):
    appointment = get_appointment(
        db=db,
        appointment_id=appointment_id
    )
    
    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún turno"
        )
    
    return appointment


@router.put(
    "/{appointment_id}",
    response_model=AppointmentResponse,
    responses={
        404: {
            "description": "No se encontró ningún turno"
        }
    },
)
def update_appointment_endpoint(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    db: Session = Depends(get_db),
):
    try:
        appointment = update_appointment(
            db=db,
            appointment_id=appointment_id,
            appointment_data=appointment_data,
        )
        
        return appointment
    except AppointmentNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún turno"
        )

    except AppointmentAvailabilityError:
        raise HTTPException(
            status_code=400,
            detail="No se encontró la disponibilidad u horario solicitado"
        )

    except AppointmentConflictError:
        raise HTTPException(
            status_code=409,
            detail="Se encontró una duplicidad en el horario o fecha solicitada"
        )

    except AppointmentCancelledError:
        raise HTTPException(
            status_code=409,
            detail="No se puede modificar un turno que ya fue cancelado"
        )


@router.patch(
    "/{appointment_id}",
    response_model=AppointmentResponse,
    responses={
        404: {
            "description": "No se encontró ningún turno"
        }
    },
)
def patch_appointment_endpoint(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    db: Session = Depends(get_db),
):
    try:
        appointment = update_appointment(
            db=db,
            appointment_id=appointment_id,
            appointment_data=appointment_data,
        )
        
        return appointment
    except AppointmentNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún turno"
        )

    except AppointmentAvailabilityError:
        raise HTTPException(
            status_code=400,
            detail="No se encontró la disponibilidad u horario solicitado"
        )

    except AppointmentConflictError:
        raise HTTPException(
            status_code=409,
            detail="Se encontró una duplicidad en el horario o fecha solicitada"
        )

    except AppointmentCancelledError:
        raise HTTPException(
            status_code=409,
            detail="No se puede modificar un turno que ya fue cancelado"
        )


@router.delete(
    "/{appointment_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ningún turno"
        }
    },
)
def delete_appointment_endpoint(
    appointment_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_appointment(
        db=db,
        appointment_id=appointment_id,
    )
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún turno"
        )
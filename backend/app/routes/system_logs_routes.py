from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.system_logs_schema import SystemLogCreate, SystemLogResponse
from app.services.system_log_service import create_system_log, get_system_log, get_system_logs

router = APIRouter(
    prefix="/system_logs",
    tags=["System Logs"],
)

@router.post(
    "/",
    response_model=SystemLogResponse
)
def create_system_log_endpoint(
    system_log_data: SystemLogCreate,
    db: Session = Depends(get_db),
):
    system_log = create_system_log(
        db=db,
        system_log_data=system_log_data
    )
    return system_log
    


@router.get("/", response_model=list[SystemLogResponse])
def get_system_logs_endpoint(
    db: Session = Depends(get_db)
):
    return get_system_logs(
        db=db
        )


@router.get(
    "/{system_log_id}",
    response_model=SystemLogResponse,
    responses={
        404: {
            "description": "No se encontró ningún registro."
        }
    },
)
def get_system_log_endpoint(
    system_log_id: int,
    db: Session = Depends(get_db)
):
    system_log = get_system_log(
        db=db,
        system_log_id=system_log_id
    )
    
    if system_log is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún registro."
        )
    
    return system_log
    
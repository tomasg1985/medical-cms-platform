from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.audit_logs_schema import AuditLogResponse, AuditLogCreate
from app.services.audit_log_service import create_audit_log, get_audit_log, get_audit_logs

router = APIRouter(
    prefix="/audit_logs",
    tags=["Audit Logs"],
)

@router.post(
    "/",
    response_model=AuditLogResponse
)
def create_audit_log_endpoint(
    audit_log_data: AuditLogCreate,
    db: Session = Depends(get_db)
):
    
    audit_log = create_audit_log(
        db=db,
        audit_log_data=audit_log_data
    )
    return audit_log


@router.get("/", response_model=list[AuditLogResponse])
def get_audit_logs_endpoint(
    db: Session = Depends(get_db)
):
    return get_audit_logs(
        db=db
    )
    

@router.get(
    "/{audit_log_id}",
    response_model=AuditLogResponse,
    responses={
        404: {
            "description": "No se encontró ningún registro."
        }
    },
)
def get_audit_log_endpoint(
    audit_log_id: int,
    db: Session = Depends(get_db)
):
    audit_log = get_audit_log(
        db=db,
        audit_log_id=audit_log_id
    )
    
    if audit_log is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún registro."
        )
    
    return audit_log
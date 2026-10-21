from sqlalchemy.orm import Session

from datetime import datetime, timezone

from app.models.audit_logs_model import AuditLog
from app.repositories.audit_logs_repository import AuditLogRepository
from app.schemas.audit_logs_schema import AuditLogCreate

audit_log_repository =  AuditLogRepository()


def create_audit_log(
    db: Session,
    audit_log_data: AuditLogCreate
) -> AuditLog | None:
    
    audit_log = AuditLog(
        **audit_log_data.model_dump(),
        occurred_at=datetime.now(timezone.utc)
    )
    
    audit_log = audit_log_repository.create(
        db=db,
        audit_log=audit_log
    )
    
    return audit_log
    
    
def get_audit_logs(
    db: Session
) -> list[AuditLog]:
    
    return audit_log_repository.get_audit_logs(
        db=db
    )
    
    
def get_audit_log(
    db: Session,
    audit_log_id: int
) -> AuditLog | None:
    
    return audit_log_repository.get_by_id(
        db=db,
        audit_log_id=audit_log_id
        
    )
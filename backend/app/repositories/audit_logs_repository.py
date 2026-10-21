from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_logs_model import AuditLog

class AuditLogRepository:
    def get_by_id(self, db: Session, audit_log_id: int) -> AuditLog | None:
        statement = (
            select(AuditLog)
            .where(AuditLog.id == audit_log_id)
        )
        result = db.execute(statement)
        audit_log = result.scalar_one_or_none()
        
        return audit_log
    
    
    def get_audit_logs(self, db: Session) -> list[AuditLog]:
        statement = select(AuditLog)
        result = db.execute(statement)
        audit_logs = result.scalars().all()
        
        return audit_logs
    
    
    def create(self, db: Session, audit_log: AuditLog) -> AuditLog:
        try:
            db.add(audit_log)
            db.commit()
            db.refresh(audit_log)

            return audit_log
        except Exception:
            db.rollback()
            raise
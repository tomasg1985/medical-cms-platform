from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.system_logs_model import SystemLog

class SystemLogRepository:
    def get_by_id(self, db: Session, system_log_id: int) -> SystemLog | None:
        statement = (
            select(SystemLog)
            .where(SystemLog.id == system_log_id)
        )
        result = db.execute(statement)
        system_log = result.scalar_one_or_none()
        
        return system_log
    

    def get_system_logs(self, db: Session) -> list[SystemLog]:
        statement = select(SystemLog)
        result = db.execute(statement)
        system_logs = result.scalars().all()
        
        return system_logs

    def create(self, db: Session, system_log: SystemLog) -> SystemLog:
        try:
            db.add(system_log)
            db.commit()
            db.refresh(system_log)

            return system_log
        except Exception:
            db.rollback()
            raise
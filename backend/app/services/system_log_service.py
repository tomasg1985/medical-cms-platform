from sqlalchemy.orm import Session

from datetime import datetime, timezone

from app.models.system_logs_model import SystemLog
from app.repositories.system_logs_repository import SystemLogRepository
from app.schemas.system_logs_schema import SystemLogCreate

system_log_repository = SystemLogRepository()


def create_system_log(
    db: Session,
    system_log_data: SystemLogCreate
) -> SystemLog | None:
    
    system_log = SystemLog(
        **system_log_data.model_dump(),
        occurred_at=datetime.now(timezone.utc)
    )
    
    system_log = system_log_repository.create(
        db=db,
        system_log=system_log
    )
    
    return system_log


def get_system_logs(
    db: Session
) -> list[SystemLog]:
    
    return system_log_repository.get_system_logs(
        db=db
    )


def get_system_log(
    db: Session,
    system_log_id: int
) -> SystemLog | None:
    
    return system_log_repository.get_by_id(
        db=db,
        system_log_id=system_log_id
    )
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permission_model import Permission

class PermissionRepository:
    def get_by_id(self, db: Session, permission_id: int) -> Permission | None:
        statement = (
            select(Permission)
            .where(Permission.id == permission_id)
        )
        result = db.execute(statement)
        permission = result.scalar_one_or_none()
    
        return permission


    def get_permissions(self, db: Session) -> list[Permission]:
        statement = select(Permission)
        result = db.execute(statement)
        permissions = result.scalars().all()
    
        return permissions


    def create(self, db: Session, permission: Permission) -> Permission:
        try:
            db.add(permission)
            db.commit()
            db.refresh(permission)

            return permission
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, permission: Permission) -> Permission:
        try:
            db.commit()
            db.refresh(permission)

            return permission
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, permission: Permission) -> bool:
        try:
            db.delete(permission)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
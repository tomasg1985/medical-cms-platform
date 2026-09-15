from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role_permission_model import RolePermission

class RolePermissionRepository:

    def create(
        self, 
        db: Session, 
        role_permission: RolePermission
    ) -> RolePermission:

        try:
            db.add(role_permission)
            db.commit()
            db.refresh(role_permission)

            return role_permission

        except Exception:
            db.rollback()
            raise


    def get_by_role_and_permission(
        self, 
        db: Session,
        role_id: int,
        permission_id: int
    ) -> RolePermission | None:

        statement = select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id
        )
        result = db.execute(statement)
        role_permission = result.scalar_one_or_none()

        return role_permission


    def delete(self, db: Session, role_permission_data: RolePermission) -> bool:
        
        try:
            db.delete(role_permission_data)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_role_model import UserRole

class UserRoleRepository:
    
    def create(
        self,
        db: Session,
        user_role: UserRole
    ) -> UserRole:
        
        try:
            db.add(user_role)
            db.commit()
            db.refresh(user_role)

            return user_role

        except Exception:
            db.rollback()
            raise


    def get_by_user_and_role(
        self,
        db: Session,
        user_id: int,
        role_id: int
    ) -> UserRole | None:
        
        statement = select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        )
        result = db.execute(statement)
        user_role = result.scalar_one_or_none()
        
        return user_role


    def delete(self, db: Session, user_role_data: UserRole) -> bool:
        
        try:
            db.delete(user_role_data)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role_model import Role

class RoleRepository:
    def get_by_id(self, db: Session, role_id: int) -> Role | None:
        statement = (
            select(Role)
            .where(Role.id == role_id)
        )
        result = db.execute(statement)
        role = result.scalar_one_or_none()
    
        return role


    def get_roles(self, db: Session) -> list[Role]:
        statement = select(Role)
        result = db.execute(statement)
        roles = result.scalars().all()
    
        return roles


    def create(self, db: Session, role: Role) -> Role:
        try:
            db.add(role)
            db.commit()
            db.refresh(role)

            return role
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, role: Role) -> Role:
        try:
            db.commit()
            db.refresh(role)

            return role
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, role: Role) -> bool:
        try:
            db.delete(role)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
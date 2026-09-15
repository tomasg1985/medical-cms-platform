from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_model import User

class UserRepository:
    def get_by_id(self, db: Session, user_id: int) -> User | None:
        statement = (
            select(User)
            .where(User.id == user_id)
        )
        result = db.execute(statement)
        user = result.scalar_one_or_none()
        
        return user


    def get_users(self, db: Session) -> list[User]:
        statement = select(User)
        result = db.execute(statement)
        users = result.scalars().all()
        
        return users


    def create(self, db: Session, user: User) -> User:
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            
            return user
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, user: User) -> User:
        try:
            db.commit()
            db.refresh(user)

            return user

        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, user: User) -> bool:
        try:
            db.delete(user)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_clinic_model import UserClinic

class UserClinicRepository:
    
    def create(
        self,
        db: Session,
        user_clinic: UserClinic
    ) -> UserClinic:
        
        try:
            db.add(user_clinic)
            db.commit()
            db.refresh(user_clinic)

            return user_clinic

        except Exception:
            db.rollback()
            raise


    def get_by_user_and_clinic(
        self,
        db: Session,
        user_id: int,
        clinic_id: int
    ) -> UserClinic | None:
        
        statement = select(UserClinic).where(
            UserClinic.user_id == user_id,
            UserClinic.clinic_id == clinic_id
        )
        result = db.execute(statement)
        user_clinic = result.scalar_one_or_none()
        
        return user_clinic


    def delete(self, db: Session, user_clinic_data: UserClinic) -> bool:
        
        try:
            db.delete(user_clinic_data)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
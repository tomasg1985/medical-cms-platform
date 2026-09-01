from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.specialty_model import Specialty

class SpecialtyRepository:
    def get_by_id(self, db: Session, specialty_id: int) -> Specialty | None:
        statement = select(Specialty).where(Specialty.id == specialty_id)
        result = db.execute(statement)
        specialty = result.scalar_one_or_none()
        
        return specialty


    def get_specialties(self, db: Session) -> list[Specialty]:
        statement = select(Specialty)
        result = db.execute(statement)
        specialties = result.scalars().all()
        
        return specialties


    def create(self, db: Session, specialty: Specialty) -> Specialty:
        
        try:
            db.add(specialty)
            db.commit()
            db.refresh(specialty)

            return specialty

        except Exception:
            db.rollback()
            raise
        
    
    def update(self, db: Session, specialty: Specialty) -> Specialty:
        
        try:
            db.commit()
            db.refresh(specialty)

            return specialty

        except Exception:
            db.rollback()
            raise
        
    
    def delete(self, db: Session, specialty: Specialty) -> bool:
        
        try:
            db.delete(specialty)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
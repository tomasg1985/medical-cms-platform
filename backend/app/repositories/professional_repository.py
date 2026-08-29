from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.professional_model import Professional
from app.models.clinic_model import Clinic

class ProfessionalRepository:
    def get_by_id(self, db: Session, professional_id: int) -> Professional | None:
        statement = select(Professional).options(selectinload(Professional.clinics)).where(Professional.id == professional_id)
        result = db.execute(statement)
        professional = result.scalar_one_or_none()

        return professional


    def get_professionals(self, db: Session) -> list[Professional]:
        statement = select(Professional).options(selectinload(Professional.clinics))
        result = db.execute(statement)
        professionals = result.scalars().all()

        return professionals


    def create(self, db: Session, professional: Professional) -> Professional:

        try:
            db.add(professional)
            db.commit()
            db.refresh(professional)
            
            return professional

        except Exception:
            db.rollback()
            raise


    def add_clinic(self, db: Session, professional: Professional, clinic: Clinic) -> Professional:

        try:
            professional.clinics.append(clinic)

            db.commit()
            db.refresh(professional)

            return professional

        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, professional: Professional) -> Professional:

        try:
            db.commit()
            db.refresh(professional)

            return professional

        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, professional: Professional) -> bool:
        
        try:
            db.delete(professional)
            db.commit()

            return True

        except Exception:
            db.rollback()
            raise
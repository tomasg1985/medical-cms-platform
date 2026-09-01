from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.medical_specialty_model import ProfessionalSpecialty

class ProfessionalSpecialtyRepository:
    
    def create(self, db: Session, professional_specialty: ProfessionalSpecialty) -> ProfessionalSpecialty:
        
        try:
            db.add(professional_specialty)
            db.commit()
            db.refresh(professional_specialty)

            return professional_specialty

        except Exception:
            db.rollback()
            raise
        
    def get_by_professional_and_specialty(self, db: Session, professional_id: int, specialty_id: int) -> ProfessionalSpecialty | None:
        statement = select(ProfessionalSpecialty).where(ProfessionalSpecialty.professional_id == professional_id, ProfessionalSpecialty.specialty_id == specialty_id)
        result = db.execute(statement)
        professional_specialty = result.scalar_one_or_none()
        
        return professional_specialty
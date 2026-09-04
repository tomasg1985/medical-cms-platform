from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.clinic_specialty_model import ClinicSpecialty

class ClinicSpecialtyRepository:
    
    def create_clinic_specialty(self, db: Session, clinic_specialty: ClinicSpecialty) -> ClinicSpecialty:
        
        try:
            db.add(clinic_specialty)
            db.commit()
            db.refresh(clinic_specialty)

            return clinic_specialty

        except Exception:
            db.rollback()
            raise

    def get_by_clinic_and_specialty(self, db: Session, clinic_id: int, specialty_id: int) -> ClinicSpecialty | None:
        statement = select(ClinicSpecialty).where(ClinicSpecialty.clinic_id == clinic_id, ClinicSpecialty.specialty_id == specialty_id)
        result = db.execute(statement)
        clinic_specialty = result.scalar_one_or_none()
        
        return clinic_specialty
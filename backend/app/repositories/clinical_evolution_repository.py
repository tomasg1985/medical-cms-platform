from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.clinical_evolution_model import ClinicalEvolution

class ClinicalEvolutionRerpository:
    def get_by_id(self, db: Session, clinical_evolution_id: int) -> ClinicalEvolution | None:
        statement = (
            select(ClinicalEvolution)
            .where(ClinicalEvolution.id == clinical_evolution_id)
        )
        result = db.execute(statement)
        clinical_evolution = result.scalar_one_or_none()
        
        return clinical_evolution


    def get_clinical_evolutions(self, db: Session) -> list[ClinicalEvolution]:
        statement = select(ClinicalEvolution)
        result = db.execute(statement)
        clinical_evolutions = result.scalars().all()
        
        return clinical_evolutions
    
    def get_by_medical_professional_appointment(
        self,
        db: Session,
        medical_record_id: int,
        professional_id: int,
        appointment_id: int
    ) -> ClinicalEvolution | None:
        
        statement = select(ClinicalEvolution).where(
            ClinicalEvolution.medical_record_id == medical_record_id,
            ClinicalEvolution.professional_id == professional_id,
            ClinicalEvolution.appointment_id == appointment_id
        )
        result = db.execute(statement)
        medical_professional_appointment = result.scalar_one_or_none()
        
        return medical_professional_appointment


    def create(self, db: Session, clinical_evolution: ClinicalEvolution) -> ClinicalEvolution:
        try:
            db.add(clinical_evolution)
            db.commit()
            db.refresh(clinical_evolution)
            
            return clinical_evolution
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, clinical_evolution: ClinicalEvolution) -> ClinicalEvolution:
        try:
            db.commit()
            db.refresh(clinical_evolution)

            return clinical_evolution
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, clinical_evolution: ClinicalEvolution) -> bool:
        try:
            db.delete(clinical_evolution)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
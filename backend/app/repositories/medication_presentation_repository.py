from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.medication_presentation_model import MedicationPresentation


class MedicationPresentationRepository:
    def get_by_id(self, db: Session, medication_presentation_id: int) -> MedicationPresentation | None:
        statement = (
            select(MedicationPresentation)
            .where(MedicationPresentation.id == medication_presentation_id)
        )
        result = db.execute(statement)
        medication_presentation = result.scalar_one_or_none()

        return medication_presentation


    def get_medication_presentations(self, db: Session) -> list[MedicationPresentation]:
        statement = select(MedicationPresentation)
        result = db.execute(statement)
        medication_presentations = result.scalars().all()

        return medication_presentations


    def get_by_medication_id(
        self,
        db: Session,
        medication_id: int
    ) -> list[MedicationPresentation]:

        statement = select(MedicationPresentation).where(
            MedicationPresentation.medication_id == medication_id
        )
        result = db.execute(statement)
        medication_presentations = result.scalars().all()
        
        return medication_presentations



    def create(self, db: Session, medication_presentation: MedicationPresentation) -> MedicationPresentation:
        try:
            db.add(medication_presentation)
            db.commit()
            db.refresh(medication_presentation)
            
            return medication_presentation
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, medication_presentation: MedicationPresentation) -> MedicationPresentation:
        try:
            db.commit()
            db.refresh(medication_presentation)

            return medication_presentation
        except Exception:
            db.rollback()
            raise
        
    def delete(self, db: Session, medication_presentation: MedicationPresentation) -> bool:
        try:
            db.delete(medication_presentation)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
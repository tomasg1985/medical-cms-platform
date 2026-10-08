from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.study_model import Study

class StudyRepository:
    def get_by_id(self, db: Session, study_id: int) -> Study | None:
        statement = (
            select(Study)
            .where(Study.id == study_id)
        )
        result = db.execute(statement)
        study = result.scalar_one_or_none()

        return study


    def get_studies(self, db: Session) -> list[Study]:
        statement = select(Study)
        result = db.execute(statement)
        studies = result.scalars().all()
    
        return studies


    def create(self, db: Session, study: Study) -> Study:
        try:
            db.add(study)
            db.commit()
            db.refresh(study)

            return study
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, study: Study) -> Study:
        try:
            db.commit()
            db.refresh(study)

            return study
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, study: Study) -> bool:
        try:
            db.delete(study)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
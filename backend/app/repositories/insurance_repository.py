from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.insurance_model import Insurance

class InsuranceRepository:
    def get_by_id(self, db: Session, insurance_id: int) -> Insurance | None:
        statement = (
            select(Insurance)
            .where(Insurance.id == insurance_id)
        )
        result = db.execute(statement)
        insurance = result.scalar_one_or_none()
        
        return insurance


    def get_by_registration(
        self,
        db: Session,
        registration: str
    ) -> Insurance | None:

        statement = (
            select(Insurance)
            .where(Insurance.registration == registration)
        )

        result = db.execute(statement)
        insurance = result.scalar_one_or_none()

        return insurance


    def get_insurances(self, db: Session) -> list[Insurance]:
        statement = select(Insurance)
        result = db.execute(statement)
        insurances = result.scalars().all()
        
        return insurances


    def create(self, db: Session, insurance: Insurance) -> Insurance:
        try:
            db.add(insurance)
            db.commit()
            db.refresh(insurance)
            
            return insurance
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, insurance: Insurance) -> Insurance:
        try:
            db.commit()
            db.refresh(insurance)

            return insurance
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, insurance: Insurance) -> bool:
            try:
                db.delete(insurance)
                db.commit()
                
                return True
            
            except Exception:
                db.rollback()
                raise
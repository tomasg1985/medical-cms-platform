from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.insurance_plan_model import InsurancePlan
from app.models.plan_model import Plan

class InsurancePlanRepository:
    
    def get_by_id(self, db: Session, insurance_plan_id: int) -> InsurancePlan | None:
        statement = (
            select(InsurancePlan)
            .where(InsurancePlan.id == insurance_plan_id)
        )
        result = db.execute(statement)
        insurance_plan = result.scalar_one_or_none()
        
        return insurance_plan


    def get_insurance_plans(self, db: Session) -> list[InsurancePlan]:
        statement =  select(InsurancePlan)
        result = db.execute(statement)
        insurance_plans = result.scalars().all()
        
        return insurance_plans


    def create(
        self, 
        db: Session,
        insurance_plan: InsurancePlan
    ) -> InsurancePlan:

        try:
            db.add(insurance_plan)
            db.commit()
            db.refresh(insurance_plan)

            return insurance_plan
        except Exception:
            db.rollback()
            raise


    def get_by_insurance_plan(
        self,
        db: Session,
        insurance_id: int,
        plan_id: int
    ) -> InsurancePlan | None:
        
        statement = select(InsurancePlan).where(
            InsurancePlan.insurance_id == insurance_id,
            InsurancePlan.plan_id == plan_id
        )
        result = db.execute(statement)
        insurance_plan = result.scalar_one_or_none()
        
        return insurance_plan



    def get_by_insurance_and_plan_name(
        self,
        db: Session,
        insurance_id: int,
        plan_name: str
    ) -> InsurancePlan | None:
        
        statement = (
            select(InsurancePlan)
            .join(Plan)
            .where(
                InsurancePlan.insurance_id == insurance_id,
                Plan.name == plan_name
            )
        )
        result = db.execute(statement)
        insurance_plan_name = result.scalar_one_or_none()
        
        return insurance_plan_name



    def delete(self, db: Session, insurance_plan_data: InsurancePlan) -> bool:
        try:
            db.delete(insurance_plan_data)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.plan_model import Plan

class PlanRepository:
    def get_by_id(self, db: Session, plan_id: int) -> Plan | None:
        statement = (
            select(Plan)
            .where(Plan.id == plan_id)
        )
        result = db.execute(statement)
        plan = result.scalar_one_or_none()
        
        return plan

    def get_plans(self, db: Session) -> list[Plan]:
        statement = select(Plan)
        result = db.execute(statement)
        plans = result.scalars().all()
        
        return plans


    def create(self, db: Session, plan: Plan) -> Plan:
        try:
            db.add(plan)
            db.commit()
            db.refresh(plan)
            
            return plan
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, plan: Plan) -> Plan:
        try:
            db.commit()
            db.refresh(plan)

            return plan
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, plan: Plan) -> bool:
            try:
                db.delete(plan)
                db.commit()
                
                return True
            
            except Exception:
                db.rollback()
                raise
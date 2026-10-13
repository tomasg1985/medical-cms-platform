from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.module_model import Module

class ModuleRepository:
    def get_by_id(self, db: Session, module_id: int) -> Module | None:
        statement = (
            select(Module)
            .where(Module.id == module_id)
        )
        result = db.execute(statement)
        module = result.scalar_one_or_none()
        
        return module
    
    
    def get_modules(self, db: Session) -> list[Module]:
        statement =  select(Module)
        result = db.execute(statement)
        modules = result.scalars().all()
        
        return modules
    
    
    def create(self, db: Session, module: Module) -> Module:
        try:
            db.add(module)
            db.commit()
            db.refresh(module)

            return module
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, module: Module) -> Module:
        try:
            db.commit()
            db.refresh(module)

            return module
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, module: Module) -> bool:
        try:
            db.delete(module)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise

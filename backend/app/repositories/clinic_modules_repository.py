from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.clinic_modules_model import ClinicModule

class ClinicModuleRepository:
    def get_by_id(self, db: Session, clinic_id: int, module_id: int) -> ClinicModule | None:
        statement = (
            select(ClinicModule)
            .where(
                ClinicModule.clinic_id == clinic_id,
                ClinicModule.module_id == module_id
            )
        )
        result = db.execute(statement)
        clinic_module = result.scalar_one_or_none()
        
        return clinic_module


    def get_clinic_modules(self, db: Session) -> list[ClinicModule]:
        statement = select(ClinicModule)
        result = db.execute(statement)
        clinic_modules = result.scalars().all()
        
        return clinic_modules
    
    
    def create(self, db: Session, clinic_module: ClinicModule) -> ClinicModule:
        try:
            db.add(clinic_module)
            db.commit()
            db.refresh(clinic_module)

            return clinic_module
        except Exception:
            db.rollback()
            raise
        
    
    def update(self, db: Session, clinic_module: ClinicModule) -> ClinicModule:
        try:
            db.commit()
            db.refresh(clinic_module)

            return clinic_module
        except Exception:
            db.rollback()
            raise
        
        
    def delete(self, db: Session, clinic_module: ClinicModule) -> bool:
        try:
            db.delete(clinic_module)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
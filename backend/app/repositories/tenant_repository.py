from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tenant_model import Tenant

class TenantRepository:
    def get_by_id(self, db: Session, tenant_id: int) -> Tenant | None:
        statement = (
            select(Tenant)
            .where(Tenant.id == tenant_id)
        )
        result = db.execute(statement)
        tenant = result.scalar_one_or_none()
    
        return tenant


    def get_tenants(self, db: Session) -> list[Tenant]:
        statement = select(Tenant)
        result = db.execute(statement)
        tenants = result.scalars().all()

        return tenants


    def create(self, db: Session, tenant: Tenant) -> Tenant:
        try:
            db.add(tenant)
            db.commit()
            db.refresh(tenant)

            return tenant
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, tenant: Tenant) -> Tenant:
        try:
            db.commit()
            db.refresh(tenant)

            return tenant
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, tenant: Tenant) -> bool:
        try:
            db.delete(tenant)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise
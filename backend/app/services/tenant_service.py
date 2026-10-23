from sqlalchemy.orm import Session

from app.models.tenant_model import Tenant
from app.repositories.tenant_repository import TenantRepository

tenant_repository = TenantRepository()

def create_tenant(
    db: Session,
    name: str,
    status: str
) -> Tenant:
    
    tenant = Tenant(
        name=name,
        status=status
    )
    
    tenant = tenant_repository.create(
        db=db,
        tenant=tenant
    )
    
    return tenant


def get_tenants(db: Session) -> list[Tenant]:
    
    tenants = tenant_repository.get_tenants(
        db=db
    )
    
    return tenants


def get_tenant(db: Session, tenant_id: int) -> Tenant | None:
    
    tenant = tenant_repository.get_by_id(
        db=db,
        tenant_id=tenant_id
    )
    
    return tenant


def update_tenant(db: Session, tenant_id: int, name: str, status: str) -> Tenant | None:
    
    tenant = get_tenant(
        db=db,
        tenant_id=tenant_id
    )
    
    if tenant is None:
        return None
    
    tenant.name = name
    tenant.status = status

    tenant = tenant_repository.update(
        db=db,
        tenant=tenant
    )
    
    return tenant


def delete_tenant(db: Session, tenant_id: int) -> bool:
    
    tenant = get_tenant(
        db=db,
        tenant_id=tenant_id
    )
    
    if tenant is None:
        return False
    
    return tenant_repository.delete(
        db=db,
        tenant=tenant
    )

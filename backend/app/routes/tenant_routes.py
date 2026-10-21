from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.tenant_schema import TenantCreate, TenantUpdate, TenantResponse
from app.services.tenant_service import create_tenant, get_tenant, get_tenants, update_tenant, delete_tenant

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)

@router.post("/", response_model=TenantResponse)
def create_tenant_endpoint(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db)
):
    try:
        tenant = create_tenant(
            db=db,
            tenant_data=tenant_data
        )

        return tenant
    except:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un usuario asociado a esta cuenta."
        )
        

@router.get("/", response_model=list[TenantResponse])
def get_tenants_endpoint(
    db: Session =  Depends(get_db)
):
    return get_tenants(db=db)


@router.get(
    "/{tenant_id}",
    response_model=TenantResponse,
    responses={
        404: {
            "description": "Ya existe un usuario asociado a esta cuenta."
        }
    },
)
def get_tenant_endpoint(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    try:
        tenant = get_tenant(
            db=-db,
            tenant_id=tenant_id
        )
        
        if tenant is None:
            raise HTTPException(
                status_code=404,
                detail="Ya existe un módulo con este nombre."
            )
            
        return tenant
    except:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un módulo con este nombre."
        )
        

@router.put(
    "/{tenant_id}",
    response_model=TenantResponse,
    responses={
        404: {
            "description": "Ya existe un usuario asociado a esta cuenta."
        }
    },
)
def update_tenant_endpoint(
    tenant_id: int,
    tenant_data: TenantUpdate,
    db: Session = Depends(get_db)
):
    try:
        tenant = update_tenant(
            db=db,
            tenant_data=tenant_data
        )
        
        if tenant is None:
            raise HTTPException(
                status_code=404,
                detail="Ya existe un módulo con este nombre."
            )
            
        return tenant
    except:
        raise HTTPException(
            status_code=404,
            detail="Ya existe un módulo con este nombre."
        )

@router.delete(
    "/{tenant_id}",
    status_code=204,
    responses={
        404: {
            "description": "Ya existe un usuario asociado a esta cuenta."
        }
    },
)
def delete_tenant_endpoint(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    try:
        deleted = delete_tenant(
            db=db,
            tenant_id=tenant_id
        )
        
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="No  se encontró ningún usuario asociado a esta cuenta."
            )
    except:
        raise HTTPException(
            status_code=404,
            detail="No  se encontró ningún usuario asociado a esta cuenta."
        )
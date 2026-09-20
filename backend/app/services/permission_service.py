from sqlalchemy.orm import Session

from app.models.permission_model import Permission
from app.repositories.permission_repository import PermissionRepository

permission_repository = PermissionRepository()

def create_permission(
    db: Session,
    name: str,
    description: str,
    resource: str,
    action: str
) -> Permission:
    
    permission = Permission(
        name=name,
        description=description,
        resource=resource,
        action=action,
        is_active=False
    )
    
    permission = permission_repository.create(
        db=db,
        permission=permission
    )
    
    return permission


def get_permissions(
    db: Session
) -> list[Permission]:
    
    permissions = permission_repository.get_permissions(
        db=db
    )
    
    return permissions


def get_permission(
    db: Session,
    permission_id: int
) -> Permission | None:
    
    permission = permission_repository.get_by_id(
        db=db,
        permission_id=permission_id
    )
    
    return permission


def update_permission(
    db: Session,
    permission_id: int,
    name: str,
    description: str,
    resource: str,
    action: str
) -> Permission | None:
    
    permission = get_permission(
        db=db,
        permission_id=permission_id
    )
    
    if permission is None:
        return permission
    
    permission.name = name
    permission.description = description
    permission.resource = resource
    permission.action = action
    
    permission = permission_repository.update(
        db=db,
        permission=permission
    )
    
    return permission


def delete_permission(
    db: Session,
    permission_id: int
) -> bool:
    
    permission = get_permission(
        db=db,
        permission_id=permission_id
    )
    
    if permission is None:
        return False
    
    return permission_repository.delete(
        db=db,
        permission=permission
    )
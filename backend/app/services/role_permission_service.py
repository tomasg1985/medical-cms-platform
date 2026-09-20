from sqlalchemy.orm import Session

from app.models.role_permission_model import RolePermission

from app.repositories.role_permission_repository import RolePermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.permission_repository import PermissionRepository

from app.core.exceptions import RolePermissionAlreadyAssociatedError

role_permission_repository = RolePermissionRepository()
role_repository = RoleRepository()
permission_repository = PermissionRepository()

def create_role_permission(
    db: Session,
    role_id: int,
    permission_id: int
) -> RolePermission | None:
    
    role = role_repository.get_by_id(
        db=db,
        role_id=role_id
    )
    
    if role is None:
        return None
    
    permission = permission_repository.get_by_id(
        db=db,
        permission_id=permission_id
    )
    
    if permission is None:
        return None
    
    existing = role_permission_repository.get_by_role_and_permission(
        db=db,
        role_id=role_id,
        permission_id=permission_id
    )
    
    if existing is not None:
        raise RolePermissionAlreadyAssociatedError()
    
    role_permission = RolePermission(
        role_id=role_id,
        permission_id=permission_id
    )
    
    role_permission = role_permission_repository.create(
        db=db,
        role_permission=role_permission
    )
    
    return role_permission
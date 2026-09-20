from sqlalchemy.orm import Session

from app.models.role_model import Role
from app.repositories.role_repository import RoleRepository

role_repository = RoleRepository()

def create_role(
    db: Session,
    name: str,
    description: str
) -> Role:

    role = Role(
        name=name,
        description=description,
        is_active=False
    )

    role = role_repository.create(
        db=db,
        role=role
    )

    return role


def get_roles(
    db: Session
) -> list[Role]:

    roles = role_repository.get_roles(
        db=db,
    )

    return roles


def get_role(
    db: Session,
    role_id: int
) -> Role | None:

    role = role_repository.get_by_id(
        db=db,
        role_id=role_id
    )

    return role


def update_role(
    db: Session,
    role_id: int,
    name: str,
    description: str
    ) -> Role | None:

    role = get_role(
        db=db,
        role_id=role_id
    )

    if role is None:
        return role

    role.name = name
    role.description = description

    role = role_repository.update(
        db=db,
        role=role
    )

    return role


def delete_role(
    db: Session,
    role_id: int
    ) -> bool:
    
    role = get_role(
        db=db,
        role_id=role_id
    )
    
    if role is None:
        return False
    
    return role_repository.delete(
        db=db,
        role=role
    )
    
from sqlalchemy.orm import Session

from app.models.user_role_model import UserRole

from app.repositories.user_role_repository import UserRoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository

from app.core.exceptions import UserRoleAlreadyAssociatedError

user_role_repository = UserRoleRepository()
user_repository = UserRepository()
role_repository = RoleRepository()

def create_user_role(
    db: Session,
    user_id: int,
    role_id: int
    ) -> UserRole | None:


    user = user_repository.get_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        return None

    role = role_repository.get_by_id(
        db=db,
        role_id=role_id
    )

    if role is None:
        return None

    existing = user_role_repository.get_by_user_and_role(
        db=db,
        user_id=user_id,
        role_id=role_id
    )

    if existing is not None:
        raise UserRoleAlreadyAssociatedError()

    user_role = UserRole(
        user_id=user_id,
        role_id=role_id
    )

    user_role = user_role_repository.create(
        db=db,
        user_role=user_role
    )

    return user_role
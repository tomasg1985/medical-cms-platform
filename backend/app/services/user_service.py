from sqlalchemy.orm import Session

from app.models.user_model import User
from app.repositories.user_repository import UserRepository

user_repository = UserRepository()


def create_user(
    db: Session,
    email: str
) -> User:
    
    user = User(
        email=email,
        is_active=False
    )
    
    user = user_repository.create(
        db=db,
        user=user
    )
    
    return user


def get_users(
    db: Session
) -> list[User]:
    
    users = user_repository.get_users(
        db=db,
    )
    
    return users


def get_user(
    db: Session,
    user_id: int
) -> User | None:
    
    user = user_repository.get_by_id(
        db=db,
        user_id=user_id
    )
    
    return user


def update_user(
    db: Session,
    user_id: int,
    email: str
) -> User | None:
    
    user = get_user(
        db=db,
        user_id=user_id,
    )
    
    if user is None:
        return None
    
    user.email = email
    
    user = user_repository.update(
        db=db,
        user=user
    )
    
    return user


def delete_user(
    db: Session,
    user_id: int
) -> bool:
    
    user = get_user(
        db=db,
        user_id=user_id,
    )
    
    if user is None:
        return False
    
    return user_repository.delete(
        db=db,
        user=user
    )
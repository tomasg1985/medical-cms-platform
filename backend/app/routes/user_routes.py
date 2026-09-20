from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.services.user_service import create_user, get_user, get_users, update_user, delete_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/", response_model=UserResponse)
def create_user_endpoint(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):

    user = create_user(
        db=db,
        email=user_data.email
    )

    return user


@router.get("/", response_model=list[UserResponse])
def get_users_endpoint(
    db: Session = Depends(get_db),
):
    users = get_users(db)
    
    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        404: {
            "description": "No se encontró ningún usuario"
        }
    },
)
def get_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):

    user = get_user(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún usuario",
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        404: {
            "description": "No se encontró ningún usuario",
        }
    },
)
def update_user_endpoint(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
):

    user = update_user(
        db=db,
        user_id=user_id,
        user_data=user_data,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún usuario",
        )

    return user

@router.delete(
    "/{user_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ningún usuario",
        }
    },
)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_user(
        db=db,
        user_id=user_id,
    )
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún usuario",
        )
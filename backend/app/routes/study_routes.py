from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.study_schema import StudyCreate, StudyResponse, StudyUpdate
from app.services.study_service import create_study, get_studies, get_study, update_study, delete_study

router = APIRouter(
    prefix="/studies",
    tags=["Studies"]
)

@router.post("/", response_model=StudyResponse)
def create_study_endpoint(
    study_data: StudyCreate,
    db: Session = Depends(get_db)
):
    return create_study(
        db=db,
        study_data=study_data
    )
    

@router.get("/", response_model=list[StudyResponse])
def get_studies_endpoint(
    db: Session = Depends(get_db)
):
    return get_studies(db=db)


@router.get(
    "/{study_id}",
    response_model= StudyResponse,
    responses={
        404: {
            "description": "No se encontró ningun estudio a su busqueda."
        }
    },
)
def get_study_endpoint(
    study_id: int,
    db: Session = Depends(get_db)
):
    study = get_study(
        db=db,
        study_id=study_id
    )
    
    if study is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningun estudio a su busqueda."
        )
        
    return study


@router.put(
    "/{study_id}",
    response_model=StudyResponse,
    responses={
        404: {
            "description": "No se encontró ningun estudio a su busqueda."
        }
    },
)
def update_study_endpoint(
    study_id: int,
    study_data: StudyUpdate,
    db: Session = Depends(get_db)
):
    study = update_study(
        db=db,
        study_id=study_id,
        study_data=study_data
    )
    
    if study is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningun estudio a su busqueda."
        )
        
    return study


@router.delete(
    "/{study_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ningun estudio a su busqueda."
        }
    },
)
def delete_study_endpoint(
    study_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_study(
        db=db,
        study_id=study_id
    )
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningun estudio a su busqueda."
        )
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import (
    AppointmentNotFoundError,
    MedicalRecordNotFoundException,
    PatientNotFoundError,
    ProfessionalNotFoundError,
    StudyNotFoundException,
)
from app.database import get_db
from app.schemas.study_schema import StudyCreate, StudyResponse, StudyUpdate
from app.services.study_service import create_study, delete_study, get_studies, get_study, update_study

router = APIRouter(
    prefix="/studies",
    tags=["Studies"],
)


@router.post(
    "/",
    response_model=StudyResponse,
    responses={
        404: {
            "description": "No se encontró una de las entidades asociadas al estudio."
        }
    },
)
def create_study_endpoint(
    study_data: StudyCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_study(
            db=db,
            study_data=study_data,
        )
    except PatientNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el paciente indicado para el estudio.",
        )
    except ProfessionalNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el profesional indicado para el estudio.",
        )
    except MedicalRecordNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la historia clínica indicada para el estudio.",
        )
    except AppointmentNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el turno indicado para el estudio.",
        )


@router.get("/", response_model=list[StudyResponse])
def get_studies_endpoint(
    db: Session = Depends(get_db)
):
    return get_studies(db=db)


@router.get(
    "/{study_id}",
    response_model=StudyResponse,
    responses={404: {"description": "No se encontró el estudio solicitado."}},
)
def get_study_endpoint(
    study_id: int,
    db: Session = Depends(get_db),
):
    try:
        study = get_study(
            db=db,
            study_id=study_id,
        )
        
        return study
    except StudyNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el estudio solicitado.",
        )


@router.put(
    "/{study_id}",
    response_model=StudyResponse,
    responses={
        404: {
            "description": "No se encontró el estudio solicitado."
        }
    },
)
def update_study_endpoint(
    study_id: int,
    study_data: StudyUpdate,
    db: Session = Depends(get_db),
):
    try:
        study =  update_study(
            db=db,
            study_id=study_id,
            study_data=study_data,
        )
        
        return study
    except StudyNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el estudio que desea actualizar.",
        )


@router.delete(
    "/{study_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró el estudio solicitado."
        }
    },
)
def delete_study_endpoint(
    study_id: int,
    db: Session = Depends(get_db),
):
    try:
        delete_study(
            db=db,
            study_id=study_id,
        )
    except StudyNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el estudio que desea eliminar.",
        )

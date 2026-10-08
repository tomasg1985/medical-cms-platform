from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.medical_document_schema import MedicalDocumentCreate, MedicalDocumentResponse, MedicalDocumentUpdate
from app.services.medical_document_service import create_medical_document, get_medical_document, get_medical_documents, update_medical_document, delete_medical_document
from app.core.exceptions import ClinicNotFoundError, MedicalDocumentAlreadyExistsException, MedicalDocumentNotFoundException, MedicalRecordNotFoundException, PatientNotFoundError, ProfessionalNotFoundError

router = APIRouter(
    prefix="/medical_documents",
    tags=["Medical Documents"]
)

@router.post(
    "/",
    response_model=MedicalDocumentResponse,
    responses={
        404: {"description": "No se encontró uno de los recursos asociados al documento."},
        409: {"description": "Ya existe un documento para esta combinación de paciente, profesional, clínica e historia clínica."},
    },
)
def create_medical_document_endpoint(
    medical_document_data: MedicalDocumentCreate,
    db: Session = Depends(get_db)
):
    try:
        medical_document = create_medical_document(
            db=db,
            medical_document_data=medical_document_data
        )
        
        return medical_document
    except PatientNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró el paciente indicado para el documento."
        )
    except ProfessionalNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró el profesional indicado para el documento."
        )
    except ClinicNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró la clínica indicada para el documento."
        )
    except MedicalRecordNotFoundException:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró la historia clínica indicada para el documento."
        )
    except MedicalDocumentAlreadyExistsException:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un documento asociado a este paciente, profesional, clínica e historia clínica.",
        )


@router.get("/", response_model=list[MedicalDocumentResponse])
def get_medical_documents_endpoint(
    db: Session = Depends(get_db)
):
    return get_medical_documents(db)


@router.get(
    "/{medical_document_id}",
    response_model=MedicalDocumentResponse,
    responses={
        404: {
            "description": "No se encontró el documento asociado a su busqueda"
        }
    },
)
def get_medical_document_endpoint(
    medical_document_id: int,
    db: Session = Depends(get_db)
):
    try:
        medical_document =  get_medical_document(
            db=db,
            medical_document_id=medical_document_id
        )
        
        return medical_document
    except MedicalDocumentNotFoundException:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró el documento solicitado."
        )


@router.put(
    "/{medical_document_id}",
    response_model=MedicalDocumentResponse,
    responses={
        404: {
            "description": "No se encontró el documento asociado a su busqueda"
        }
    },
)
def update_medical_document_endpoint(
    medical_document_id: int,
    medical_document_data: MedicalDocumentUpdate,
    db: Session = Depends(get_db)
):
    try:
        medical_document =  update_medical_document(
            db=db,
            medical_document_id=medical_document_id,
            medical_document_data=medical_document_data
        )
        
        return medical_document
    except MedicalDocumentNotFoundException:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró el documento que desea actualizar."
        )


@router.delete(
    "/{medical_document_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró el documento asociado a su busqueda"
        }
    },
)
def delete_medical_document_endpoint(
    medical_document_id: int,
    db: Session = Depends(get_db)
):
    
    try:
        delete_medical_document(
            db=db,
            medical_document_id=medical_document_id
        )
    except MedicalDocumentNotFoundException:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró el documento que desea eliminar."
        )
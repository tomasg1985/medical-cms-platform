from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.medical_document_schema import MedicalDocumentCreate, MedicalDocumentResponse, MedicalDocumentUpdate
from app.services.medical_document_service import create_medical_document, get_medical_document, get_medical_documents, update_medical_document, delete_medical_document

router = APIRouter(
    prefix="/medical_documents",
    tags=["Medical Documents"]
)

@router.post("/", response_model=MedicalDocumentResponse)
def create_medical_document_endpoint(
    medical_document_data: MedicalDocumentCreate,
    db: Session = Depends(get_db)
):
    return create_medical_document(
        db=db,
        medical_document_data=medical_document_data
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
    medical_document = get_medical_document(
        db=db,
        medical_document_id=medical_document_id
    )
    
    if medical_document is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el documento asociado a su busqueda"
        )
        
    return medical_document


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
    medical_document = update_medical_document(
        db=db,
        medical_document_id=medical_document_id,
        medical_document_data=medical_document_data
    )
    
    if medical_document is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el documento asociado a su busqueda"
        )
        
    return medical_document


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
    
    deleted = delete_medical_document(
        db=db,
        medical_document_id=medical_document_id
    )
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el documento asociado a su busqueda"
        )
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.patient_contact_schema import (
    PatientContactCreate,
    PatientContactResponse,
    PatientContactUpdate,
)
from app.services.patient_contact_service import (
    create_patient_contact,
    get_patient_contact,
    get_patient_contacts,
    update_patient_contact,
    delete_patient_contacts,
)

router = APIRouter(
    prefix="/patient-contacts",
    tags=["Patient Contacts"],
)


@router.post(
    "/",
    response_model=PatientContactResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contact(
    contact_data: PatientContactCreate,
    db: Session = Depends(get_db),
):
    contact = create_patient_contact(
        db=db,
        patient_contact_data=contact_data,
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    return contact


@router.get(
    "/",
    response_model=list[PatientContactResponse],
)
def list_contacts(db: Session = Depends(get_db)):
    return get_patient_contacts(db=db)


@router.get(
    "/{patient_contact_id}",
    response_model=PatientContactResponse,
)
def read_contact(
    patient_contact_id: int,
    db: Session = Depends(get_db),
):
    contact = get_patient_contact(
        db=db,
        patient_contact_id=patient_contact_id,
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient contact not found",
        )

    return contact


@router.put(
    "/{patient_contact_id}",
    response_model=PatientContactResponse,
)
def update_contact(
    patient_contact_id: int,
    contact_data: PatientContactUpdate,
    db: Session = Depends(get_db),
):
    contact = update_patient_contact(
        db=db,
        patient_contact_id=patient_contact_id,
        patient_contact_data=contact_data,
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient contact not found",
        )

    return contact


@router.delete(
    "/{patient_contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_contact(
    patient_contact_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_patient_contacts(
        db=db,
        patient_contact_id=patient_contact_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient contact not found",
        )

    return None

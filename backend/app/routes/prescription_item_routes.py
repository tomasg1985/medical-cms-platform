from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.prescription_item_schema import (
    PrescriptionItemCreate,
    PrescriptionItemResponse,
    PrescriptionItemUpdate,
)
from app.services.prescription_item_service import (
    create_prescription_item,
    delete_prescription_item,
    get_prescription_item,
    get_prescription_items,
    update_prescription_item,
)

router = APIRouter(
    prefix="/prescription_items",
    tags=["Prescription Items"],
)


@router.post("/", response_model=PrescriptionItemResponse)
def create_prescription_item_endpoint(
    prescription_id: int,
    medication_id: int,
    prescription_item_data: PrescriptionItemCreate,
    db: Session = Depends(get_db),
):
    created = create_prescription_item(
        db=db,
        prescription_id=prescription_id,
        medication_id=medication_id,
        prescription_item_data=prescription_item_data,
    )

    if created is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la receta o el medicamento asociado.",
        )

    return created


@router.get("/", response_model=list[PrescriptionItemResponse])
def get_prescription_items_endpoint(
    db: Session = Depends(get_db),
):
    return get_prescription_items(db=db)


@router.get(
    "/{prescription_item_id}",
    response_model=PrescriptionItemResponse,
    responses={
        404: {
            "description": "No se encontró ninguna item asociado a su receta médica."
        }
    },
)
def get_prescription_item_endpoint(
    prescription_item_id: int,
    db: Session = Depends(get_db),
):
    prescription_item = get_prescription_item(
        db=db,
        prescription_item_id=prescription_item_id,
    )

    if prescription_item is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna item asociado a su receta médica.",
        )

    return prescription_item


@router.put(
    "/{prescription_item_id}",
    response_model=PrescriptionItemResponse,
    responses={
        404: {
            "description": "No se encontró ninguna item asociado a su receta médica."
        }
    },
)
def update_prescription_item_endpoint(
    prescription_item_id: int,
    prescription_item_data: PrescriptionItemUpdate,
    db: Session = Depends(get_db),
):
    prescription_item = update_prescription_item(
        db=db,
        prescription_item_id=prescription_item_id,
        prescription_item_data=prescription_item_data,
    )

    if prescription_item is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna item asociado a su receta médica.",
        )

    return prescription_item


@router.delete(
    "/{prescription_item_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró ninguna item asociado a su receta médica."
        }
    },
)
def delete_prescription_item_endpoint(
    prescription_item_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_prescription_item(
        db=db,
        prescription_item_id=prescription_item_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna item asociado a su receta médica.",
        )

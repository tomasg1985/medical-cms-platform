from sqlalchemy.orm import Session

from app.models.prescription_item_model import PrescriptionItem
from app.models.prescription_model import Prescription
from app.models.medication_model import Medication

from app.schemas.prescription_item_schema import PrescriptionItemCreate, PrescriptionItemUpdate

from app.repositories.prescription_item_repository import PrescriptionItemRepository

prescription_item_repository = PrescriptionItemRepository()

def create_prescription_item(
    db: Session,
    prescription_id: int,
    medication_id: int,
    prescription_item_data: PrescriptionItemCreate
) -> PrescriptionItem | None:

    prescription = db.get(Prescription, prescription_id)
    if prescription is None:
        return None

    medication = db.get(Medication, medication_id)
    if medication is None:
        return None

    prescription_item = PrescriptionItem(
        dosage=prescription_item_data.dosage,
        frequency=prescription_item_data.frequency,
        duration=prescription_item_data.duration,
        instructions=prescription_item_data.instructions,
        prescription_id=prescription_id,
        medication_id=medication_id,
    )

    prescription_item = prescription_item_repository.create(
        db=db,
        prescription_item=prescription_item,
    )

    return prescription_item


def get_prescription_items(
    db: Session,
) -> list[PrescriptionItem]:

    return prescription_item_repository.get_prescription_items(
        db=db,
    )


def get_prescription_item(
    db: Session,
    prescription_item_id: int,
) -> PrescriptionItem | None:

    return prescription_item_repository.get_by_id(
        db=db,
        prescription_item_id=prescription_item_id,
    )


def update_prescription_item(
    db: Session,
    prescription_item_id: int,
    prescription_item_data: PrescriptionItemUpdate,
) -> PrescriptionItem | None:

    prescription_item = get_prescription_item(
        db=db,
        prescription_item_id=prescription_item_id,
    )

    if prescription_item is None:
        return None

    data = prescription_item_data.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(prescription_item, field, value)

    prescription_item = prescription_item_repository.update(
        db=db,
        prescription_item=prescription_item,
    )

    return prescription_item


def delete_prescription_item(
    db: Session,
    prescription_item_id: int,
) -> bool:

    prescription_item = get_prescription_item(
        db=db,
        prescription_item_id=prescription_item_id,
    )

    if prescription_item is None:
        return False

    return prescription_item_repository.delete(
        db=db,
        prescription_item=prescription_item,
    )
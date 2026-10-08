from sqlalchemy.orm import Session

from app.models.medication_presentation_model import MedicationPresentation

from app.repositories.medication_presentation_repository import MedicationPresentationRepository
from app.repositories.medication_repository import MedicationRepository
from app.schemas.medication_presentation_schema import (
    MedicationPresentationCreate,
    MedicationPresentationUpdate,
)

medication_presentation_repository = MedicationPresentationRepository()
medication_repository = MedicationRepository()


def create_medical_presentation(
    db: Session,
    medication_id: int,
    presentation_data: MedicationPresentationCreate,
) -> MedicationPresentation | None:

    medication = medication_repository.get_by_id(
        db=db,
        medication_id=medication_id
    )

    if medication is None:
        return None

    medication_presentation = MedicationPresentation(
        presentation=presentation_data.presentation,
        concentration=presentation_data.concentration,
        quantity=presentation_data.quantity,
        unit=presentation_data.unit,
        status=presentation_data.status,
        medication_id=medication_id,
    )

    medication_presentation = medication_presentation_repository.create(
        db=db,
        medication_presentation=medication_presentation,
    )

    return medication_presentation


create_medication_presentation = create_medical_presentation


def get_medication_presentations(
    db: Session,
) -> list[MedicationPresentation]:

    return medication_presentation_repository.get_medication_presentations(
        db=db,
    )


def get_medication_presentation(
    db: Session,
    medication_presentation_id: int,
) -> MedicationPresentation | None:

    return medication_presentation_repository.get_by_id(
        db=db,
        medication_presentation_id=medication_presentation_id,
    )


def medication_presentation(
    db: Session,
    medication_presentation_id: int,
) -> MedicationPresentation | None:

    return get_medication_presentation(
        db=db,
        medication_presentation_id=medication_presentation_id,
    )


def update_medication_presentation(
    db: Session,
    medication_presentation_id: int,
    medication_presentation_data: MedicationPresentationUpdate,
) -> MedicationPresentation | None:

    medication_presentation = medication_presentation_repository.get_by_id(
        db=db,
        medication_presentation_id=medication_presentation_id,
    )

    if medication_presentation is None:
        return None

    medication_presentation.presentation = medication_presentation_data.presentation
    medication_presentation.concentration = medication_presentation_data.concentration
    medication_presentation.quantity = medication_presentation_data.quantity
    medication_presentation.unit = medication_presentation_data.unit
    medication_presentation.status = medication_presentation_data.status

    medication_presentation = medication_presentation_repository.update(
        db=db,
        medication_presentation=medication_presentation,
    )

    return medication_presentation


def delete_medication_presentation(
    db: Session,
    medication_presentation_id: int,
) -> bool:

    medication_presentation = get_medication_presentation(
        db=db,
        medication_presentation_id=medication_presentation_id,
    )

    if medication_presentation is None:
        return False

    return medication_presentation_repository.delete(
        db=db,
        medication_presentation=medication_presentation,
    )

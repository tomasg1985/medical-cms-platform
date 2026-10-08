from types import SimpleNamespace
from unittest.mock import patch

from app.schemas.medication_presentation_schema import MedicationPresentationCreate
from app.services.medication_presentation_service import create_medical_presentation


def test_create_medical_presentation_assigns_fields_and_medication_id():
    medication = SimpleNamespace(id=7)
    payload = MedicationPresentationCreate(
        presentation="Caja",
        concentration="500 mg",
        quantity="10",
        unit="comprimidos",
        status="active",
    )

    def fake_create(db, medication_presentation):
        return medication_presentation

    with patch(
        "app.services.medication_presentation_service.medication_repository.get_by_id",
        return_value=medication,
    ), patch(
        "app.services.medication_presentation_service.medication_presentation_repository.create",
        side_effect=fake_create,
    ):
        created = create_medical_presentation(
            db=None,
            medication_id=7,
            presentation_data=payload,
        )

    assert created is not None
    assert created.presentation == "Caja"
    assert created.concentration == "500 mg"
    assert created.quantity == "10"
    assert created.unit == "comprimidos"
    assert created.status == "active"
    assert created.medication_id == 7

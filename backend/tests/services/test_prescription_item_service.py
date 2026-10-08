from types import SimpleNamespace
from unittest.mock import patch

from app.services.prescription_item_service import get_prescription_items


def test_get_prescription_items_returns_list():
    items = [SimpleNamespace(id=1), SimpleNamespace(id=2)]

    with patch(
        "app.services.prescription_item_service.prescription_item_repository.get_prescription_items",
        return_value=items,
    ):
        result = get_prescription_items(db=None)

    assert result == items
    assert isinstance(result, list)

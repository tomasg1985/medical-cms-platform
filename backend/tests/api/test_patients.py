from datetime import date


def patient_payload(**overrides):
    data = {
        "name": "Ana",
        "last_name": "Perez",
        "birth_date": "1990-05-15",
        "dni": "TEST-PATIENT-1001",
        "email": "ana.perez.test@example.com",
        "phone": "1100000000",
        "address": "Calle de prueba 123",
        "insurance": "Cobertura de prueba",
    }
    data.update(overrides)
    return data


def test_list_patients_empty(client):
    response = client.get("/patients/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_patient_not_found(client):
    response = client.get("/patients/999999999")
    assert response.status_code == 404


def test_create_and_get_patient(client):
    payload = patient_payload()
    response = client.post("/patients/", json=payload)
    assert response.status_code == 200, response.text

    created = response.json()
    assert created["name"] == payload["name"]
    assert created["dni"] == payload["dni"]
    assert created["birth_date"] == payload["birth_date"]
    assert created["clinics"] == []

    get_response = client.get(f"/patients/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == payload["email"]


def test_update_patient_preserves_unmodified_fields(client):
    response = client.post(
        "/patients/",
        json=patient_payload(dni="TEST-PATIENT-1002"),
    )
    assert response.status_code == 200, response.text
    patient_id = response.json()["id"]

    update_response = client.put(
        f"/patients/{patient_id}",
        json={"name": "Nombre actualizado"},
    )
    assert update_response.status_code == 200, update_response.text
    updated = update_response.json()
    assert updated["name"] == "Nombre actualizado"
    assert updated["last_name"] == "Perez"
    assert updated["email"] == "ana.perez.test@example.com"


def test_update_patient_not_found(client):
    response = client.put(
        "/patients/999999999",
        json={"name": "Nombre actualizado"},
    )
    assert response.status_code == 404


def test_create_patient_missing_required_fields(client):
    response = client.post("/patients/", json={"name": "Ana"})
    assert response.status_code == 422


def test_delete_patient(client):
    response = client.post(
        "/patients/",
        json=patient_payload(dni="TEST-PATIENT-1003"),
    )
    assert response.status_code == 200, response.text
    patient_id = response.json()["id"]

    delete_response = client.delete(f"/patients/{patient_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/patients/{patient_id}")
    assert get_response.status_code == 404


def test_delete_patient_not_found(client):
    response = client.delete("/patients/999999999")
    assert response.status_code == 404
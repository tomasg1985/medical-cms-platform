from app.database import get_db
from app.main import app
from app.models.tenant_model import Tenant
from app.models.clinic_model import Clinic


def crear_clinica_de_prueba():
    dependency = app.dependency_overrides[get_db]
    db_generator = dependency()
    db = next(db_generator)

    try:
        tenant = Tenant(name="Tenant test asociaciones", status="active")
        db.add(tenant)
        db.flush()

        clinic = Clinic(name="Clinica test asociaciones", tenant_id=tenant.id)
        db.add(clinic)
        db.commit()
        db.refresh(clinic)
        return clinic.id
    finally:
        db.close()
        db_generator.close()


def crear_paciente(client):
    response = client.post(
        "/patients/",
        json={
            "name": "Ana",
            "last_name": "Test",
            "dni": "98765432",
            "email": "ana.test@example.com",
            "phone": "1122334455",
            "address": "Direccion de prueba",
            "insurance": "Obra social test",
        },
    )
    assert response.status_code == 200, response.text
    return response.json()["id"]


def test_asociar_paciente_a_clinica(client):
    patient_id = crear_paciente(client)
    clinic_id = crear_clinica_de_prueba()
    response = client.post(f"/patients/{patient_id}/clinics/{clinic_id}")

    assert response.status_code == 200, response.text
    assert response.json()["patient_id"] == patient_id
    assert response.json()["clinic_id"] == clinic_id


def test_paciente_inexistente_devuelve_404(client):
    clinic_id = crear_clinica_de_prueba()
    response = client.post(f"/patients/-1/clinics/{clinic_id}")
    assert response.status_code == 404


def test_clinica_inexistente_devuelve_404(client):
    patient_id = crear_paciente(client)
    response = client.post(f"/patients/{patient_id}/clinics/-1")
    assert response.status_code == 404


def test_asociacion_duplicada_devuelve_409(client):
    patient_id = crear_paciente(client)
    clinic_id = crear_clinica_de_prueba()
    url = f"/patients/{patient_id}/clinics/{clinic_id}"

    primera = client.post(url)
    assert primera.status_code == 200, primera.text

    segunda = client.post(url)
    assert segunda.status_code == 409

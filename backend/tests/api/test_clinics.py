from app.database import get_db
from app.main import app
from app.models.tenant_model import Tenant


def create_test_tenant(name="Tenant test clinics"):
    dependency = app.dependency_overrides[get_db]
    db_generator = dependency()
    db = next(db_generator)

    try:
        tenant = Tenant(name=name, status="active")
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        return tenant.id
    finally:
        db.close()
        db_generator.close()


def create_test_clinic(client):
    tenant_id = create_test_tenant()
    response = client.post(
        "/clinics/",
        json={
            "name": "Clinica test",
            "tenant_id": tenant_id,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_create_clinic_with_existing_tenant(client):
    tenant_id = create_test_tenant("Tenant para crear clinica")

    response = client.post(
        "/clinics/",
        json={
            "name": "Clinica nueva",
            "tenant_id": tenant_id,
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Clinica nueva"
    assert isinstance(data["id"], int)


def test_create_clinic_with_missing_tenant_returns_404(client):
    response = client.post(
        "/clinics/",
        json={
            "name": "Clinica sin tenant",
            "tenant_id": -1,
        },
    )

    assert response.status_code == 404


def test_get_clinic_not_found(client):
    response = client.get("/clinics/999999999")
    assert response.status_code == 404


def test_update_clinic(client):
    clinic = create_test_clinic(client)

    response = client.put(
        f"/clinics/{clinic['id']}",
        json={"name": "Clinica actualizada"},
    )

    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Clinica actualizada"


def test_delete_clinic(client):
    clinic = create_test_clinic(client)

    response = client.delete(f"/clinics/{clinic['id']}")
    assert response.status_code == 204

    get_response = client.get(f"/clinics/{clinic['id']}")
    assert get_response.status_code == 404

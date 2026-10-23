from uuid import uuid4

def tenant_payload():
    return {
        "name": f"tenant-test-{uuid4().hex}",
        "status": "active",
    }


def test_create_and_get_tenant(client):
    payload = tenant_payload()

    response = client.post("/tenants/", json=payload)

    assert response.status_code == 200
    created = response.json()
    assert created["name"] == payload["name"]
    assert created["status"] == payload["status"]
    assert "id" in created
    assert "created_at" in created
    assert "updated_at" in created

    response = client.get(f"/tenants/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_list_tenants(client):
    payload = tenant_payload()
    created_response = client.post("/tenants/", json=payload)

    assert created_response.status_code == 200
    tenant_id = created_response.json()["id"]

    response = client.get("/tenants/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(tenant["id"] == tenant_id for tenant in response.json())


def test_update_tenant(client):
    payload = tenant_payload()
    created_response = client.post("/tenants/", json=payload)

    assert created_response.status_code == 200
    tenant_id = created_response.json()["id"]

    updated_payload = {
        "name": f"tenant-updated-{uuid4().hex}",
        "status": "inactive",
    }

    response = client.put(
        f"/tenants/{tenant_id}",
        json=updated_payload,
    )

    assert response.status_code == 200
    assert response.json()["name"] == updated_payload["name"]
    assert response.json()["status"] == updated_payload["status"]


def test_delete_tenant(client):
    payload = tenant_payload()
    created_response = client.post("/tenants/", json=payload)

    assert created_response.status_code == 200
    tenant_id = created_response.json()["id"]

    response = client.delete(f"/tenants/{tenant_id}")

    assert response.status_code == 204

    response = client.get(f"/tenants/{tenant_id}")
    assert response.status_code == 404


def test_get_missing_tenant_returns_404(client):
    response = client.get("/tenants/2147483647")

    assert response.status_code == 404


def test_update_missing_tenant_returns_404(client):
    response = client.put(
        "/tenants/2147483647",
        json=tenant_payload(),
    )

    assert response.status_code == 404


def test_delete_missing_tenant_returns_404(client):
    response = client.delete("/tenants/2147483647")

    assert response.status_code == 404


def test_list_audit_logs_returns_200_and_empty_list(client):
    response = client.get("/audit_logs/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_audit_log_not_found_returns_404(client):
    response = client.get("/audit_logs/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No se encontró ningún registro."
    }

def test_create_audit_log_returns_200_or_201(client):
    payload = {
        "action": "CREATE",
        "resource_type": "patient",
        "outcome": "success"
    }

    response = client.post("/audit_logs/", json=payload)

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["id"] is not None
    assert data["action"] == payload["action"]
    assert data["resource_type"] == payload["resource_type"]
    assert data["outcome"] == payload["outcome"]
    assert data["occurred_at"] is not None
    assert data["resource_id"] is None
    assert data["request_id"] is None
    assert data["metadata_"] == {}
    
    
def test_get_audit_log_by_id_returns_200(client):
    payload = {
        "action": "CREATE",
        "resource_type": "patient",
        "outcome": "success"
    }

    create_response = client.post("/audit_logs/", json=payload)

    assert create_response.status_code in (200, 201)

    audit_log_id = create_response.json()["id"]

    response = client.get(f"/audit_logs/{audit_log_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == audit_log_id
    assert data["action"] == payload["action"]
    assert data["resource_type"] == payload["resource_type"]
    assert data["outcome"] == payload["outcome"]
    assert data["occurred_at"] is not None
    
    
def test_create_audit_log_without_required_fields_returns_422(client):
    payload = {
        "action": "CREATE"
    }

    response = client.post("/audit_logs/", json=payload)

    assert response.status_code == 422
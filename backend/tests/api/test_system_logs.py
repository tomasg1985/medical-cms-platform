
def test_list_system_logs_returns_200_and_empty_list(client):
    response = client.get("/system_logs/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_system_log_not_found_returns_404(client):
    response = client.get("/system_logs/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No se encontró ningún registro."
    }


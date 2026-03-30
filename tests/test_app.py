from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_get_tasks():
    res = client.get("/tasks")
    assert res.status_code == 200


def test_create_task():
    res = client.post("/tasks", json={
        "id": 0,
        "title": "Test Task",
        "done": False
    })
    assert res.status_code == 200
    assert res.json()["title"] == "Test Task"


def test_not_found():
    res = client.get("/tasks/9999")
    assert res.status_code == 404

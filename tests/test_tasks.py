import sqlalchemy
import pytest
from fastapi.testclient import TestClient
from app import app
import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_engine = sqlalchemy.create_engine(f"sqlite:///{tmp_path}/test.db")
    monkeypatch.setattr(app_module, "engine", test_engine)
    with TestClient(app) as client:
        yield client


def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Buy milk"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["done"] == 0


def test_create_task_no_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 422


def test_update_task(client):
    client.post("/tasks", json={"title": "Buy milk"})
    response = client.patch("/tasks/1", json={"done": 1})
    assert response.status_code == 200
    assert response.json()["done"] == 1


def test_delete_task(client):
    client.post("/tasks", json={"title": "Buy milk"})
    response = client.delete("/tasks/1")
    assert response.status_code == 204


def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 404

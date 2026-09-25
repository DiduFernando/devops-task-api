import pytest
from app import create_app, db

@pytest.fixture()
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "running"

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_create_and_get_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Build Jenkins pipeline", "description": "Automate CI/CD"},
    )
    assert response.status_code == 201
    task_id = response.json["id"]

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == task_id

def test_create_task_requires_title(client):
    response = client.post("/tasks", json={"description": "Missing title"})
    assert response.status_code == 400

def test_update_task(client):
    response = client.post("/tasks", json={"title": "Original"})
    task_id = response.json["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated", "completed": True},
    )
    assert response.status_code == 200
    assert response.json["title"] == "Updated"
    assert response.json["completed"] is True

def test_delete_task(client):
    response = client.post("/tasks", json={"title": "Delete me"})
    task_id = response.json["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json == []

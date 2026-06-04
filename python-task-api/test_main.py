"""
Tests for the Task Manager API.
Run: pytest test_main.py -v
"""
import pytest
from fastapi.testclient import TestClient
from main import app, tasks, next_id

client = TestClient(app)


def setup_function():
    """Clear tasks before each test."""
    tasks.clear()
    global next_id
    import main
    main.next_id = 1


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Task Manager API" in response.json()["message"]


def test_create_task():
    response = client.post("/tasks", json={"title": "Buy groceries", "priority": 2})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["priority"] == 2
    assert data["completed"] is False
    assert data["id"] == 1


def test_get_all_tasks():
    client.post("/tasks", json={"title": "Task A", "priority": 1})
    client.post("/tasks", json={"title": "Task B", "priority": 3})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_by_id():
    client.post("/tasks", json={"title": "My Task"})
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["title"] == "My Task"


def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_update_task():
    client.post("/tasks", json={"title": "Old title"})
    response = client.patch("/tasks/1", json={"title": "New title", "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["completed"] is True


def test_delete_task():
    client.post("/tasks", json={"title": "To delete"})
    response = client.delete("/tasks/1")
    assert response.status_code == 204
    # Verify it's gone
    assert client.get("/tasks/1").status_code == 404


def test_filter_by_completed():
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    client.patch("/tasks/1", json={"completed": True})

    completed = client.get("/tasks?completed=true").json()
    pending = client.get("/tasks?completed=false").json()

    assert len(completed) == 1
    assert len(pending) == 1


def test_stats():
    client.post("/tasks", json={"title": "T1", "priority": 3})
    client.post("/tasks", json={"title": "T2", "priority": 2})
    client.patch("/tasks/1", json={"completed": True})

    response = client.get("/tasks/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["completed"] == 1
    assert data["by_priority"]["high"] == 1

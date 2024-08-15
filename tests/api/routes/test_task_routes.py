import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, create_autospec

from app.api.endpoints.task_routes import TaskRoutes  # Adjust this import based on your app's structure
from app.db.database import Database
from app.dependencies import Dependency
from app.crud.task_crud import TaskCRUD
from app.api.schemas.task_schemas import TaskCreate, Task


@pytest.fixture
def client_success():
    app = FastAPI()
    sample_task = Task(id=1, title="Test Task", description="A task for testing.", status="todo")

    # Create a mock for the TaskCRUD
    mock_task_crud = create_autospec(TaskCRUD)
    mock_task_crud.return_value.create_task.return_value = sample_task
    mock_task_crud.return_value.get_tasks.return_value = [sample_task]

    # Create a mock for the Dependency
    mock_dependency = MagicMock(spec=Dependency)

    # Initialize the TaskRoutes with mocked dependencies
    task_routes = TaskRoutes(dependency=mock_dependency, task_crud=mock_task_crud)

    # Include the router in the FastAPI app
    app.include_router(task_routes.router)

    return TestClient(app)

@pytest.fixture
def client_exception():
    app = FastAPI()
    sample_task = Task(id=1, title="Test Task", description="A task for testing.", status="todo")

    # Create a mock for the TaskCRUD
    mock_task_crud = create_autospec(TaskCRUD)
    mock_task_crud.return_value.create_task.side_effect = Exception("Simulated error")
    mock_task_crud.return_value.get_tasks.side_effect = Exception("Simulated error")

    # Create a mock for the Dependency
    mock_dependency = MagicMock(spec=Dependency)

    # Initialize the TaskRoutes with mocked dependencies
    task_routes = TaskRoutes(dependency=mock_dependency, task_crud=mock_task_crud)

    # Include the router in the FastAPI app
    app.include_router(task_routes.router)

    return TestClient(app)


def test_create_task(client_success):
    """Test successful task creation."""
    # Define the input task data
    task_data = {"title": "Test Task", "description": "A task for testing.", "status": 'todo'}
    expected_task_data = {"id": 1, "title": "Test Task", "description": "A task for testing.", "status": 'todo'}

    # Send the request to create a task
    response = client_success.post("/api/tasks/", json=task_data)

    # Assertions
    assert response.status_code == 200
    assert response.json() == expected_task_data

def test_read_tasks(client_success):
    """Test reading tasks successfully."""
    expected_tasks = [{"id": 1, "title": "Test Task", "description": "A task for testing.", "status": 'todo'}]

    # Send the request to read tasks
    response = client_success.get("/api/tasks/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == expected_tasks

def test_create_task_exception(client_exception):
    """Test handling of exceptions during task creation."""

    # Define the input task data
    task_data = {"id": 1, "title": "Test Task", "description": "A task for testing.", "status": 'todo'}

    # Send the request to create a task
    response = client_exception.post("/api/tasks/", json=task_data)

    # Assertions
    assert response.status_code == 500
    assert response.json() == {'detail': 'An error occurred while creating the task.'}

def test_read_tasks_exception(client_exception):
    """Test handling of exceptions during reading tasks."""
    # Send the request to read tasks
    response = client_exception.get("/api/tasks/")

    # Assertions
    assert response.status_code == 500
    assert response.json() == {'detail': 'An error occurred while fetching tasks.'}

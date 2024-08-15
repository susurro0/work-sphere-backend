import pytest
from unittest.mock import MagicMock
from app.models.task_models import Task  # Adjust the import based on your structure
from app.db.database import Database

@pytest.fixture
def mock_database():
    # Create a mock Database instance
    db_mock = MagicMock(spec=Database)
    db_mock.database = MagicMock()  # Mock the database attribute
    return db_mock

@pytest.fixture
def task_model(mock_database):
    # Set the mocked database to the Task model
    Task._meta.database = mock_database.database
    mock_database.database.create_tables = MagicMock()  # Mock create_tables
    return Task

def test_create_task(task_model, mock_database):
    # Arrange
    mock_database.database.create_tables([task_model])  # Ensure the table is created

    # Act: Create a task instance and save it
    task = task_model(title="Test Task", description="A task for testing", status="Pending")
    task.save()  # This will now use the mocked database

    # Assert
    mock_database.database.create_tables.assert_called_once_with([task_model])
    assert task.id is not None  # Ensure the task has been assigned an ID
    assert task.title == "Test Task"
    assert task.description == "A task for testing"
    assert task.status == "Pending"

def test_task_status(task_model):
    # Create a task instance
    task = task_model(title="Test Task", description="A task for testing", status="Pending")

    # Assert the initial status
    assert task.status == "Pending"

    # Update the status
    task.status = "Completed"

    # Assert the updated status
    assert task.status == "Completed"

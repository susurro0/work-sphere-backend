import pytest
from unittest.mock import MagicMock, patch
from app.api.schemas.task_schemas import TaskCreate
from app.models.task_models import Task
from app.crud.task_crud import TaskCRUD  # Adjust the import based on your structure

@pytest.fixture
def mock_database():
    # Create a mock Database instance
    db_mock = MagicMock()
    return db_mock

@pytest.fixture
def task_crud(mock_database):
    return TaskCRUD(mock_database)

@pytest.fixture
def mock_task():
    return MagicMock(spec=Task)

def test_create_task(task_crud, mock_task):
    # Arrange
    task_data = TaskCreate(title="Test Task", description="A task for testing", status="Pending")
    with patch('app.models.task_models.Task.create', return_value=mock_task) as mock_create:
        # Act
        created_task = task_crud.create_task(task_data)

        # Assert
        mock_create.assert_called_once_with(**task_data.model_dump())
        assert created_task == mock_task

def test_get_tasks(task_crud, mock_task):
    # Arrange
    with patch('app.models.task_models.Task.select', return_value=[mock_task]) as mock_select:
        # Act
        tasks = task_crud.get_tasks()

        # Assert
        mock_select.assert_called_once()
        assert tasks == [mock_task]

def test_get_task_found(task_crud, mock_task):
    # Arrange
    task_id = 1
    with patch('app.models.task_models.Task.get_or_none', return_value=mock_task) as mock_get:
        # Act
        task = task_crud.get_task(task_id)

        # Assert
        mock_get.assert_called_once_with(Task.id == task_id)
        assert task == mock_task

def test_get_task_not_found(task_crud):
    # Arrange
    task_id = 999  # Assume this task does not exist
    with patch('app.models.task_models.Task.get_or_none', return_value=None) as mock_get:
        # Act
        task = task_crud.get_task(task_id)

        # Assert
        mock_get.assert_called_once_with(Task.id == task_id)
        assert task is None

def test_update_task_found(task_crud, mock_task):
    # Arrange
    task_id = 1
    task_data = TaskCreate(title="Updated Task", description="Updated description", status="Completed")
    with patch('app.models.task_models.Task.get_or_none', return_value=mock_task) as mock_get, \
         patch.object(mock_task, 'save') as mock_save:
        # Act
        updated_task = task_crud.update_task(task_id, task_data)

        # Assert
        mock_get.assert_called_once_with(Task.id == task_id)
        assert updated_task == mock_task
        mock_task.save.assert_called_once()  # Ensure save was called

def test_update_task_not_found(task_crud):
    # Arrange
    task_id = 999  # Assume this task does not exist
    task_data = TaskCreate(title="Updated Task", description="Updated description", status="Completed")
    with patch('app.models.task_models.Task.get_or_none', return_value=None) as mock_get:
        # Act
        updated_task = task_crud.update_task(task_id, task_data)

        # Assert
        mock_get.assert_called_once_with(Task.id == task_id)
        assert updated_task is None  # No task found, so return should be None

def test_delete_task_found(task_crud, mock_task):
    # Arrange
    task_id = 1
    with patch('app.models.task_models.Task.get_or_none', return_value=mock_task) as mock_get, \
         patch.object(mock_task, 'delete_instance') as mock_delete:
        # Act
        result = task_crud.delete_task(task_id)

        # Assert
        mock_get.assert_called_once_with(Task.id == task_id)
        mock_delete.assert_called_once()
        assert result is True

def test_delete_task_not_found(task_crud):
    # Arrange
    task_id = 999  # Assume this task does not exist
    with patch('app.models.task_models.Task.get_or_none', return_value=None) as mock_get:
        # Act
        result = task_crud.delete_task(task_id)

        # Assert
        mock_get.assert_called_once_with(Task.id == task_id)
        assert result is False

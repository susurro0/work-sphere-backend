import pytest
from anyio.abc import TaskStatus
from pydantic import ValidationError
from enum import Enum

from app.api.schemas.task_schemas import TaskBase, TaskCreate, Task


def test_task_base_model_valid():
    task = TaskBase(title="Sample Task", description="This is a task")
    assert task.title == "Sample Task"
    assert task.description == "This is a task"
    assert task.status == "todo"

def test_task_base_model_invalid_title():
    with pytest.raises(ValidationError) as exc_info:
        TaskBase(title="A" * 101, description="This is a task")
    assert "String should have at most 100 characters" in str(exc_info.value)

def test_task_create_model():
    task_create = TaskCreate(title="New Task", description="Create a new task")
    assert task_create.title == "New Task"
    assert task_create.description == "Create a new task"
    assert task_create.status == "todo"

def test_task_model_valid():
    task = Task(id=1, title="Sample Task", description="This is a task", status="in_progress")
    assert task.id == 1
    assert task.title == "Sample Task"
    assert task.description == "This is a task"
    assert task.status == "in_progress"

def test_task_model_invalid_id():
    with pytest.raises(ValidationError) as exc_info:
        Task(id="one", title="Sample Task", description="This is a task", status="in_progress")
    assert "should be a valid integer" in str(exc_info.value)


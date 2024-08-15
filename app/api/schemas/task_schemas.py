from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    title: str = Field(max_length=100)
    description: str
    status: str = "todo"

    model_config = ConfigDict()

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)  # Updated from 'orm_mode'


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
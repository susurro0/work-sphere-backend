from typing import Optional, List
from app.api.schemas.task_schemas import TaskCreate
from app.models.task_models import Task

class TaskCRUD:
    def __init__(self, db):
        self.db = db  # The db is now an instance of SqliteDatabase

    def create_task(self, task: TaskCreate) -> Task:
        db_task = Task.create(**task.model_dump())
        return db_task

    def get_tasks(self) -> List[Task]:
        return list(Task.select())  # Returns all tasks as a list

    def get_task(self, task_id: int) -> Optional[Task]:
        return Task.get_or_none(Task.id == task_id)  # Returns None if not found

    def update_task(self, task_id: int, task_data: TaskCreate) -> Optional[Task]:
        db_task = Task.get_or_none(Task.id == task_id)
        if db_task:
            for key, value in task_data.model_dump().items():
                setattr(db_task, key, value)
            db_task.save()  # Save changes to the database
        return db_task

    def delete_task(self, task_id: int) -> bool:
        db_task = Task.get_or_none(Task.id == task_id)
        if db_task:
            db_task.delete_instance()  # Delete the task from the database
            return True
        return False

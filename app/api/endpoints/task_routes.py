from fastapi import APIRouter, HTTPException
from app.crud.task_crud import TaskCRUD
from ..schemas.task_schemas import TaskCreate, Task
from app.dependencies import Dependency

class TaskRoutes:
    def __init__(self, dependency: Dependency, task_crud=TaskCRUD):
        self.router = APIRouter()
        self.db = dependency.get_db()
        self.task_crud = task_crud

        @self.router.post("/api/tasks/", response_model=Task)
        def create_task(task: TaskCreate):
            try:
                return self.task_crud(self.db).create_task(task)
            except Exception as e:
                print(f"Failed to create task: {e}")  # Replace with proper logging in production
                raise HTTPException(status_code=500, detail="An error occurred while creating the task.")

        @self.router.get("/api/tasks/", response_model=list[Task])
        def read_tasks():
            try:
                return self.task_crud(self.db).get_tasks()
            except Exception as e:
                print(f"Failed to create task: {e}")  # Replace with proper logging in production
                raise HTTPException(status_code=500, detail="An error occurred while fetching tasks.")

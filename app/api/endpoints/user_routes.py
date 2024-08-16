from fastapi import APIRouter, HTTPException
from app.crud.user_crud import UserCRUD
from ..schemas.user_schemas import UserCreate, User
from app.dependencies import Dependency

class UserRoutes:
    def __init__(self, dependency: Dependency, user_crud=UserCRUD):
        self.router = APIRouter()
        self.db = dependency.get_db()
        self.user_crud = user_crud

        @self.router.post("/api/users/", response_model=User)
        def create_user(user: UserCreate):
            try:
                return self.user_crud(self.db).create_user(user)
            except Exception as e:
                print(f"Failed to create user: {e}")  # Replace with proper logging in production
                raise HTTPException(status_code=500, detail="An error occurred while creating the user.")

        @self.router.get("/api/users/", response_model=list[User])
        def read_users():
            try:
                return self.user_crud(self.db).get_users()
            except Exception as e:
                print(f"Failed to create user: {e}")  # Replace with proper logging in production
                raise HTTPException(status_code=500, detail="An error occurred while fetching users.")

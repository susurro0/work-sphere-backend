import logging

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.crud.user_crud import UserCRUD
from ..schemas.user_schemas import UserCreate, User, TokenResponse, UserBase
from app.dependencies import Dependency


class UserRoutes:
    def __init__(self, dependency: Dependency, user_crud=UserCRUD):
        self.router = APIRouter()
        self.db = dependency.get_db()
        self.user_crud = user_crud(self.db)
        self.auth_service = dependency.get_auth_service()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


        @self.router.get("/api/users/", response_model=list[User])
        def read_users():
            try:
                return self.user_crud.get_users()
            except Exception as e:
                logging.error(f"Failed to fetch users: {e}")
                raise HTTPException(status_code=500, detail="An error occurred while fetching users.")

        @self.router.post("/register/", response_model=UserBase)
        def register(user: UserCreate):
            if self.user_crud.get_by_username(user.username):
                raise HTTPException(status_code=400, detail="Username already registered.")
            if self.user_crud.get_by_email(user.email):
                raise HTTPException(status_code=400, detail="Email already registered.")
            try:
                return self.user_crud.create_user(user)
            except Exception as e:
                logging.error(f"Failed to register user: {e}")
                raise HTTPException(status_code=500, detail="An error occurred during registration.")

        @self.router.post("/login/", response_model=TokenResponse)
        def login(login_request: OAuth2PasswordRequestForm = Depends()):
            try:
                user = self.auth_service.authenticate_user(login_request.username, login_request.password)
                if isinstance(user, User):
                    access_token = self.auth_service.create_access_token(data={"sub": user.username})
                    return TokenResponse(access_token=access_token, token_type="bearer")
                else:
                    raise HTTPException(status_code=401, detail="Invalid credentials")
            except HTTPException as e:
                raise e
            except Exception as e:
                logging.error(f"Login failed: {e}")
                raise HTTPException(status_code=500, detail="An error occurred during login")

        @self.router.get("/users/me/", response_model=UserBase)
        def read_users_me(token: str = Depends(self.oauth2_scheme)):
            try:
                return self.auth_service.verify_token(token)
            except Exception as e:
                logging.error(f"Failed to retrieve user info: {e}")
                raise HTTPException(status_code=500, detail="Failed to retrieve user info")

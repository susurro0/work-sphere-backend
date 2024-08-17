from typing import Optional, List

from argon2 import PasswordHasher

from app.api.schemas.user_schemas import UserCreate
from app.models.user_models import User

ph = PasswordHasher()

class UserCRUD:
    def __init__(self, db):
        self.db = db  # The db is now an instance of SqliteDatabase

    def create_user(self, user: UserCreate) -> User:
        # Create a user in the database
        db_user = User.create(
            username=user.username,
            email=user.email,
            role=user.role,
            password=self._hash_password(user.password)  # Hash the password before saving
        )
        return db_user

    def get_users(self) -> List[User]:
        return list(User.select())  # Returns all users as a list

    def get_user(self, user_id: int) -> Optional[User]:
        return User.get_or_none(User.id == user_id)  # Returns None if not found

    def get_by_username(self, username: str) -> Optional[User]:
        return User.get_or_none(User.username == username)  # Returns None if not found

    def get_by_email(self, email: str) -> Optional[User]:
        return User.get_or_none(User.email == email)  # Returns None if not found

    def update_user(self, user_id: int, user_data: UserCreate) -> Optional[User]:
        db_user = User.get_or_none(User.id == user_id)
        if db_user:
            for key, value in user_data.model_dump().items():
                setattr(db_user, key, value)
            db_user.save()  # Save changes to the database
        return db_user

    def delete_user(self, user_id: int) -> bool:
        db_user = User.get_or_none(User.id == user_id)
        if db_user:
            db_user.delete_instance()  # Delete the user from the database
            return True
        return False

    def _hash_password(self, plain_password: str) -> str:
        return ph.hash(plain_password)

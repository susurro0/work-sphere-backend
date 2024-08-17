import pytest
from unittest.mock import MagicMock

from peewee import IntegrityError

from app.db.database import Database
from app.models.user_models import User


@pytest.fixture
def mock_database():
    db_mock = MagicMock(spec=Database)
    db_mock.database = MagicMock()  # Mock the database attribute
    return db_mock

@pytest.fixture
def user_model(mock_database):
    User._meta.database = mock_database.database
    mock_database.database.create_tables = MagicMock()  # Mock create_tables
    return User

def test_create_user(user_model, mock_database):
    # Arrange
    mock_database.database.create_tables([user_model])  # Ensure the table is created

    # Act: Create a task instance and save it
    user = user_model(username="testuser", email="a@a.com", password="savePassword")
    user.save()  # This will now use the mocked database

    # Assert
    mock_database.database.create_tables.assert_called_once_with([user_model])
    assert user.id is not None  # Ensure the task has been assigned an ID
    assert user.username == 'testuser'
    assert user.email == 'a@a.com'
    assert user.password == "savePassword"

def test_set_password(user_model):
    user = user_model(username="testuser", email="a@a.com", password="plainPassword")
    plain_password = "plainPassword"
    user.set_password(plain_password)
    assert user.password != plain_password  # Ensure the password is hashed
    assert user.verify_password(plain_password)

def test_default_role(user_model):
    user = user_model(username="testuser", email="a@a.com", password="savePassword1!")
    user.save()
    assert user.role == 'user'

def test_creation_timestamp(user_model):
    # Act
    user = user_model(username="testuser", email="a@a.com", password="savePassword")
    user.save()

    # Assert
    assert user.created_at is not None


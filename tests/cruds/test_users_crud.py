import pytest
from unittest.mock import MagicMock, patch

from app.api.schemas.user_schemas import UserCreate
from app.crud.user_crud import UserCRUD
from app.models.user_models import User


@pytest.fixture
def mock_database():
    # Create a mock Database instance
    db_mock = MagicMock()
    return db_mock

@pytest.fixture
def user_crud(mock_database):
    return UserCRUD(mock_database)

@pytest.fixture
def mock_user():
    return MagicMock(spec=User)


def test_create_user(user_crud, mock_user):
    user_data = UserCreate(username='username', email='a@b.com', password='Password1234!')
    hashed_password = '$argon2id$v=19$m=65536,t=3,p=4$v//lBZPMjVXwFFfxeCJR8A$GXU19Cj8007AmUriCh1qUYGKKd9Wy50t5WTTgR7tbKQ'  # Updated mock Argon2 hash

    with patch('app.crud.user_crud.PasswordHasher') as MockPasswordHasher, \
            patch('app.models.user_models.User.create', return_value=mock_user) as mock_create:
        # Setup the mock instance
        mock_hasher = MockPasswordHasher.return_value
        mock_hasher.hash.return_value = hashed_password

        created_user = user_crud.create_user(user_data)
        mock_create.assert_called_once()

        args, kwargs = mock_create.call_args
        assert 'password' in kwargs
        assert kwargs['password'] != user_data.password
        assert created_user == mock_user

def test_get_users(user_crud, mock_user):
    # Arrange
    with patch('app.models.user_models.User.select', return_value=[mock_user]) as mock_select:
        # Act
        users = user_crud.get_users()

        # Assert
        mock_select.assert_called_once()
        assert users == [mock_user]

def test_get_user_found(user_crud, mock_user):
    # Arrange
    user_id = 1
    with patch('app.models.user_models.User.get_or_none', return_value=mock_user) as mock_get:
        # Act
        user = user_crud.get_user(user_id)

        # Assert
        mock_get.assert_called_once_with(User.id == user_id)
        assert user == mock_user

def test_get_user_by_username_found(user_crud, mock_user):
    # Arrange
    username = 'username'
    with patch('app.models.user_models.User.get_or_none', return_value=mock_user) as mock_get:
        # Act
        user = user_crud.get_by_username(username)

        # Assert
        mock_get.assert_called_once_with(User.username == username)
        assert user == mock_user

def test_get_user_by_email_found(user_crud, mock_user):
    # Arrange
    email = 'a@b.com'
    with patch('app.models.user_models.User.get_or_none', return_value=mock_user) as mock_get:
        # Act
        user = user_crud.get_by_email(email)

        # Assert
        mock_get.assert_called_once_with(User.email == email)
        assert user == mock_user

def test_get_user_not_found(user_crud):
    # Arrange
    user_id = 999  # Assume this user does not exist
    with patch('app.models.user_models.User.get_or_none', return_value=None) as mock_get:
        # Act
        user = user_crud.get_user(user_id)

        # Assert
        mock_get.assert_called_once_with(User.id == user_id)
        assert user is None

def test_get_user_by_username_not_found(user_crud):
    # Arrange
    username = 'username'  # Assume this user does not exist
    with patch('app.models.user_models.User.get_or_none', return_value=None) as mock_get:
        # Act
        user = user_crud.get_by_username(username)

        # Assert
        mock_get.assert_called_once_with(User.username == username)
        assert user is None

def test_get_user_by_email_not_found(user_crud):
    # Arrange
    email = 'a@b.com'  # Assume this user does not exist
    with patch('app.models.user_models.User.get_or_none', return_value=None) as mock_get:
        # Act
        user = user_crud.get_by_email(email)

        # Assert
        mock_get.assert_called_once_with(User.email == email)
        assert user is None

def test_update_user_found(user_crud, mock_user):
    # Arrange
    user_id = 1
    user_data = UserCreate(username='username', email='a@b.com', password='Password1234!')
    with patch('app.models.user_models.User.get_or_none', return_value=mock_user) as mock_get, \
         patch.object(mock_user, 'save') as mock_save:
        # Act
        updated_user = user_crud.update_user(user_id, user_data)

        # Assert
        mock_get.assert_called_once_with(User.id == user_id)
        assert updated_user == mock_user
        mock_user.save.assert_called_once()  # Ensure save was called

def test_update_user_not_found(user_crud):
    # Arrange
    user_id = 999  # Assume this user does not exist
    user_data = UserCreate(username='username', email='a@b.com', password='Password1234!')
    with patch('app.models.user_models.User.get_or_none', return_value=None) as mock_get:
        # Act
        updated_user = user_crud.update_user(user_id, user_data)

        # Assert
        mock_get.assert_called_once_with(User.id == user_id)
        assert updated_user is None  # No user found, so return should be None

def test_delete_user_found(user_crud, mock_user):
    # Arrange
    user_id = 1
    with patch('app.models.user_models.User.get_or_none', return_value=mock_user) as mock_get, \
         patch.object(mock_user, 'delete_instance') as mock_delete:
        # Act
        result = user_crud.delete_user(user_id)

        # Assert
        mock_get.assert_called_once_with(User.id == user_id)
        mock_delete.assert_called_once()
        assert result is True

def test_delete_user_not_found(user_crud):
    # Arrange
    user_id = 999  # Assume this user does not exist
    with patch('app.models.user_models.User.get_or_none', return_value=None) as mock_get:
        # Act
        result = user_crud.delete_user(user_id)

        # Assert
        mock_get.assert_called_once_with(User.id == user_id)
        assert result is False

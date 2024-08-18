import os

import pytest
import jwt
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from peewee import DoesNotExist

from app.models.user_models import User
from app.utils.auth_service import AuthService


@pytest.fixture
def auth_service():
    """Fixture to create an AuthService instance with a mocked database."""
    mock_db = MagicMock()
    return AuthService(db=mock_db)


from datetime import datetime

from datetime import datetime, timedelta

from datetime import datetime, timedelta
import jwt


def test_create_access_token(auth_service):
    """Test creating a JWT access token."""
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = auth_service.create_access_token(data, expires_delta=expires_delta)

    # Decode the token to verify its content
    decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[auth_service.ALGORITHM])

    # Assertions
    assert decoded_token["sub"] == "testuser"
    assert "exp" in decoded_token




def test_create_access_token_with_custom_expiration(auth_service):
    """Test creating a JWT access token with a custom expiration time."""
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=10)
    token = auth_service.create_access_token(data, expires_delta)

    decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[auth_service.ALGORITHM])
    assert decoded_token["sub"] == "testuser"
    assert datetime.fromtimestamp(decoded_token["exp"]) < datetime.utcnow() + expires_delta


@patch('app.models.user_models.User.get')
def test_authenticate_user_success(mock_user_get, auth_service):
    """Test user authentication with correct credentials."""
    # Create a mock user with valid password hash
    mock_user = MagicMock(spec=User)
    mock_user.password = 'hashedpassword'  # Mock the hashed password value

    # Mock verify_password to return True
    mock_user.verify_password.return_value = True
    mock_user_get.return_value = mock_user

    # Mock the password hasher to avoid actual hashing
    with patch('argon2.PasswordHasher.verify') as mock_verify:
        mock_verify.return_value = True

        # Authenticate the user
        user = auth_service.authenticate_user("testuser", "correctpassword")

        # Assertions
        assert user == mock_user
        mock_verify.assert_called_once_with('hashedpassword', 'correctpassword')


@patch('app.models.user_models.User.get')
def test_authenticate_user_failure(mock_user_get, auth_service):
    """Test user authentication with incorrect credentials."""
    mock_user = MagicMock(spec=User)
    mock_user.verify_password.return_value = False
    mock_user_get.return_value = mock_user

    # Mock the password hasher to avoid actual hashing
    with patch('argon2.PasswordHasher.verify') as mock_verify:
        mock_verify.return_value = False
        user = auth_service.authenticate_user("testuser", "wrongpassword")

        assert user is None
        mock_verify.assert_called_once()


@patch('app.models.user_models.User.get', side_effect=DoesNotExist)
def test_authenticate_user_does_not_exist(mock_user_get, auth_service):
    """Test user authentication when user does not exist."""
    user = auth_service.authenticate_user("nonexistentuser", "password")

    assert user is None
    mock_user_get.assert_called_once_with(User.username == "nonexistentuser")


@patch('app.models.user_models.User.get')
def test_verify_token_success(mock_user_get, auth_service):
    """Test verifying a valid JWT token."""
    mock_user = MagicMock(spec=User)
    mock_user_get.return_value = mock_user

    token = auth_service.create_access_token({"sub": "testuser"})
    user = auth_service.verify_token(token)

    assert user == mock_user
    mock_user_get.assert_called_once_with(User.username == "testuser")

@patch('app.models.user_models.User.get')
def test_verify_token_invalid_token_missing_username(mock_user_get, auth_service):
    """Test verifying a valid JWT token."""
    mock_user = MagicMock(spec=User)
    mock_user_get.return_value = mock_user

    token = auth_service.create_access_token({"sub": None})
    with pytest.raises(HTTPException) as exc_info:
        auth_service.verify_token(token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"

@patch('app.models.user_models.User.get')
def test_verify_token_invalid_token(mock_user_get, auth_service):
    """Test verifying an invalid JWT token."""
    with pytest.raises(HTTPException) as exc_info:
        auth_service.verify_token("invalidtoken")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"
    mock_user_get.assert_not_called()


@patch('app.models.user_models.User.get', side_effect=DoesNotExist)
def test_verify_token_user_does_not_exist(mock_user_get, auth_service):
    """Test verifying a JWT token when the user does not exist."""
    token = auth_service.create_access_token({"sub": "nonexistentuser"})

    with pytest.raises(HTTPException) as exc_info:
        auth_service.verify_token(token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"
    mock_user_get.assert_called_once_with(User.username == "nonexistentuser")

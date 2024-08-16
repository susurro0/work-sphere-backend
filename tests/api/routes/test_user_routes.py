import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, create_autospec

from app.api.endpoints.user_routes import UserRoutes  # Adjust this import based on your app's structure
from app.db.database import Database
from app.dependencies import Dependency
from app.crud.user_crud import UserCRUD
from app.api.schemas.user_schemas import UserCreate, User


@pytest.fixture
def client_success():
    app = FastAPI()
    sample_user = User(id=1, username='username', email='a@b.com', password='password')

    # Create a mock for the UserCRUD
    mock_user_crud = create_autospec(UserCRUD)
    mock_user_crud.return_value.create_user.return_value = sample_user
    mock_user_crud.return_value.get_users.return_value = [sample_user]

    # Create a mock for the Dependency
    mock_dependency = MagicMock(spec=Dependency)

    # Initialize the UserRoutes with mocked dependencies
    user_routes = UserRoutes(dependency=mock_dependency, user_crud=mock_user_crud)

    # Include the router in the FastAPI app
    app.include_router(user_routes.router)

    return TestClient(app)

@pytest.fixture
def client_exception():
    app = FastAPI()
    sample_user = User(id=1, username='username', email='a@b.com', password='password')

    # Create a mock for the UserCRUD
    mock_user_crud = create_autospec(UserCRUD)
    mock_user_crud.return_value.create_user.side_effect = Exception("Simulated error")
    mock_user_crud.return_value.get_users.side_effect = Exception("Simulated error")

    # Create a mock for the Dependency
    mock_dependency = MagicMock(spec=Dependency)

    # Initialize the UserRoutes with mocked dependencies
    user_routes = UserRoutes(dependency=mock_dependency, user_crud=mock_user_crud)

    # Include the router in the FastAPI app
    app.include_router(user_routes.router)

    return TestClient(app)


def test_create_user(client_success):
    """Test successful user creation."""
    # Define the input user data
    user_data = {'username':'username', 'email':'a@b.com', 'password':'password'}
    expected_user_data = {'id': 1, 'username':'username', 'email':'a@b.com'}

    # Send the request to create a user
    response = client_success.post("/api/users/", json=user_data)

    # Assertions
    assert response.status_code == 200
    assert response.json() == expected_user_data

def test_read_users(client_success):
    """Test reading users successfully."""
    expected_users = [{'id': 1, 'username':'username', 'email':'a@b.com'}]

    # Send the request to read users
    response = client_success.get("/api/users/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == expected_users

def test_create_user_exception(client_exception):
    """Test handling of exceptions during user creation."""

    # Define the input user data
    user_data = {'id': 1, 'username':'username', 'email':'a@b.com', 'password':'password'}

    # Send the request to create a user
    response = client_exception.post("/api/users/", json=user_data)

    # Assertions
    assert response.status_code == 500
    assert response.json() == {'detail': 'An error occurred while creating the user.'}

def test_read_users_exception(client_exception):
    """Test handling of exceptions during reading users."""
    # Send the request to read users
    response = client_exception.get("/api/users/")

    # Assertions
    assert response.status_code == 500
    assert response.json() == {'detail': 'An error occurred while fetching users.'}

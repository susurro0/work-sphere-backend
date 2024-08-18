import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, create_autospec

from app.api.endpoints.user_routes import UserRoutes  # Adjust this import based on your app's structure
from app.dependencies import Dependency
from app.crud.user_crud import UserCRUD
from app.api.schemas.user_schemas import UserCreate, User
from app.models.user_models import User  as UserModel
from app.utils.auth_service import AuthService


@pytest.fixture
def client_success():
    app = FastAPI()
    sample_user = User(id=1, username='username', email='a@b.com', password='Password123!')
    # Create a mock for the UserCRUD
    mock_user_crud = create_autospec(UserCRUD)
    mock_user_crud.return_value.create_user.return_value = sample_user
    mock_user_crud.return_value.get_users.return_value = [sample_user]
    mock_user_crud.return_value.get_by_username.return_value = None
    mock_user_crud.return_value.get_by_email.return_value = None

    # Create a mock for the AuthService
    mock_auth_service = create_autospec(AuthService)
    mock_auth_service.authenticate_user.return_value = UserModel(id=1, username='username', email='a@b.com', role='user')
    mock_auth_service.create_access_token.return_value = 'testtoken'
    mock_auth_service.verify_token.return_value = User(id=1, username='username', email='a@b.com', role='user')
    # Create a mock for the Dependency
    mock_dependency = MagicMock(spec=Dependency)
    mock_dependency.get_auth_service.return_value = mock_auth_service
    mock_dependency.get_db.return_value = MagicMock()  # Mock database if needed

    # Initialize the UserRoutes with mocked dependencies
    user_routes = UserRoutes(dependency=mock_dependency, user_crud=mock_user_crud)

    # Include the router in the FastAPI app
    app.include_router(user_routes.router)



    return TestClient(app)

@pytest.fixture
def client_exception_500():
    app = FastAPI()

    # Create a mock for the UserCRUD
    mock_user_crud = create_autospec(UserCRUD)
    mock_user_crud.return_value.create_user.side_effect = Exception("Simulated error")
    mock_user_crud.return_value.get_users.side_effect = Exception("Simulated error")
    mock_user_crud.return_value.get_by_username.return_value = None
    mock_user_crud.return_value.get_by_email.return_value = None

    # Create a mock for the AuthService
    mock_auth_service = create_autospec(AuthService)
    mock_auth_service.verify_token.side_effect = Exception("Simulated error")

    # Create a mock for the Dependency
    mock_dependency = MagicMock(spec=Dependency)
    mock_dependency.get_auth_service.return_value = mock_auth_service
    mock_dependency.get_db.return_value = MagicMock()  # Mock database if needed

    # Initialize the UserRoutes with mocked dependencies
    user_routes = UserRoutes(dependency=mock_dependency, user_crud=mock_user_crud)

    # Include the router in the FastAPI app
    app.include_router(user_routes.router)

    return TestClient(app)

@pytest.fixture
def client():
    app = FastAPI()
    return TestClient(app)

def test_read_users(client_success):
    """Test reading users successfully."""
    expected_users = [{'id': 1, 'username':'username', 'role': 'user', 'email':'a@b.com'}]

    # Send the request to read users
    response = client_success.get("/api/users/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == expected_users

def test_register_user(client_success):
    """Test registering a user successfully."""
    user_data = {'username': 'newuser', 'email': 'a@b.com', 'password': 'Password123!'}

    # Send the request to register a new user
    response = client_success.post("/register/", json=user_data)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {'username': 'username', 'role': 'user', 'email': 'a@b.com'}

def test_read_users_exception(client_exception_500):
    """Test handling of exceptions during reading users."""
    # Send the request to read users
    response = client_exception_500.get("/api/users/")

    # Assertions
    assert response.status_code == 500
    assert response.json() == {'detail': 'An error occurred while fetching users.'}

def test_register_user_exception(client_exception_500):
    """Test handling of exceptions during user registration."""
    user_data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'Password123!'}

    # Send the request to register a new user
    response = client_exception_500.post("/register/", json=user_data)

    # Assertions
    assert response.status_code == 500
    assert response.json() == {'detail': 'An error occurred during registration.'}

def test_register_user_exception_username_exists(client):

    app = FastAPI()
    """Test handling of exceptions during user registration."""
    user_data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'Password123!'}
    sample_user = User(id=1, username='username', email='a@b.com', password='password')

    # Create a mock for the UserCRUD
    mock_user_crud = create_autospec(UserCRUD)
    mock_user_crud.return_value.get_by_username.return_value = sample_user

    # Create a mock for the Dependency
    mock_dependency = MagicMock(spec=Dependency)

    # Initialize the UserRoutes with mocked dependencies
    user_routes = UserRoutes(dependency=mock_dependency, user_crud=mock_user_crud)

    # Include the router in the FastAPI app
    app.include_router(user_routes.router)

    client = TestClient(app)
    # Send the request to register a new user
    response = client.post("/register/", json=user_data)

    # Assertions
    assert response.status_code == 400
    assert response.json() == {'detail': 'Username already registered.'}

def test_register_user_exception_email_exists(client):

    app = FastAPI()
    """Test handling of exceptions during user registration."""
    user_data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'Password123!'}
    sample_user = User(id=1, username='username', email='a@b.com', password='password')

    # Create a mock for the UserCRUD
    mock_user_crud = create_autospec(UserCRUD)
    mock_user_crud.return_value.get_by_username.return_value = None
    mock_user_crud.return_value.get_by_email.return_value = sample_user

    # Create a mock for the Dependency
    mock_dependency = MagicMock(spec=Dependency)

    # Initialize the UserRoutes with mocked dependencies
    user_routes = UserRoutes(dependency=mock_dependency, user_crud=mock_user_crud)

    # Include the router in the FastAPI app
    app.include_router(user_routes.router)

    client = TestClient(app)
    # Send the request to register a new user
    response = client.post("/register/", json=user_data)

    # Assertions
    assert response.status_code == 400
    assert response.json() == {'detail': 'Email already registered.'}

def test_login_user(client_success):
    """Test logging in a user successfully."""
    # Send the request to log in the user
    response = client_success.post("/login/", data={'username': 'username', 'password': 'Password123!'})

    # Assertions
    assert response.status_code == 200
    assert response.json() == {'access_token': 'testtoken', 'token_type': 'bearer'}

def test_login_user_exception(client_exception_500):
    """Test handling of exceptions during user login."""
    login_data = {'username': 'username', 'password': 'Password1234!'}

    # Mock the authentication and token creation methods to raise an exception
    client_exception_500.app.dependency_overrides[Dependency.get_auth_service] = lambda: MagicMock(
        authenticate_user=lambda u, p: None
    )

    # Send the request to log in the user
    response = client_exception_500.post("/login/", data=login_data)

    # Assertions
    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid credentials'}

def test_login_user_exception_500():
    """Test handling of exceptions during user login."""

    login_data = {'username': 'username', 'password': 'Password1'}
    app = FastAPI()
    sample_user = User(id=1, username='username', email='a@b.com', password='Password123!')
    # Create a mock for the UserCRUD
    mock_user_crud = create_autospec(UserCRUD)
    mock_user_crud.return_value.create_user.return_value = sample_user
    mock_user_crud.return_value.get_users.return_value = [sample_user]
    mock_user_crud.return_value.get_by_username.return_value = None
    mock_user_crud.return_value.get_by_email.return_value = None

    # Create a mock for the AuthService
    mock_auth_service = create_autospec(AuthService)
    mock_auth_service.authenticate_user.return_value = UserModel(id=1, username='username', email='a@b.com')
    mock_auth_service.create_access_token.return_value.side_effect = Exception("Error")

    # Create a mock for the Dependency
    mock_dependency = MagicMock(spec=Dependency)
    mock_dependency.get_auth_service.return_value = mock_auth_service
    mock_dependency.get_db.return_value = MagicMock()  # Mock database if needed

    # Initialize the UserRoutes with mocked dependencies
    user_routes = UserRoutes(dependency=mock_dependency, user_crud=mock_user_crud)

    # Include the router in the FastAPI app
    app.include_router(user_routes.router)


    client = TestClient(app)
    # Send the request to log in the user
    response = client.post("/login/", data=login_data)
    # Assertions
    # Assertions
    assert response.status_code == 500
    assert response.json() == {'detail': 'An error occurred during login'}

def test_get_user_me(client_success):
    """Test logging in a user successfully."""
    login_data = {'username': 'username', 'password': 'Password123!'}
    headers = {'Authorization': 'Bearer testtoken'}

    # Send the request to log in the user
    response = client_success.get("/users/me/", headers=headers)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {'username': 'username', 'role': 'user', 'email': 'a@b.com'}

def test_read_users_me_exception(client_exception_500):
    """Test handling of exceptions during retrieving user info."""
    headers = {'Authorization': 'Bearer testtoken'}

    # Send the request to read the logged-in user's info
    response = client_exception_500.get("/users/me/", headers=headers)

    # Assertions
    assert response.status_code == 500
    assert response.json() == {'detail': 'Failed to retrieve user info'}
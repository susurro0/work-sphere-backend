import pytest
from pydantic import ValidationError
from enum import Enum

from app.api.schemas.user_schemas import UserBase, UserCreate, User


def test_user_base_model_valid():
    user = UserBase(username="SampleUser", email="a@b.com")
    assert user.username == "SampleUser"
    assert user.email == "a@b.com"

@pytest.mark.parametrize("username", [
    '@adsfas',      # Contains special character '@'
    'asd adfds',    # Contains a space
    'asdfds. ',     # Contains a period '.' and a space at the end
])
def test_user_base_model_invalid_username(username):
    with pytest.raises(ValidationError) as exc_info:
        UserBase(username=username, email="a@b.com")
    assert "Username must be a single word without spaces, whitespace, or special characters." in str(exc_info.value)

@pytest.mark.parametrize("invalid_email", [
    'plainaddress',          # No @ symbol
    'plainaddress.com',      # website
    '@missingusername.com',  # Missing username
    'username@.com',         # Missing domain name
    'username@com',          # Missing period in domain
    'username@domain..com',  # Double period in domain
])
def test_user_base_model_invalid_email(invalid_email):
    with pytest.raises(ValidationError) as exc_info:
        UserBase(username='username', email=invalid_email)
    assert "value is not a valid email address" in str(exc_info.value)

@pytest.mark.parametrize("username, email, password", [
    ('user1', 'user1@example.com', 'password1'),  # Valid case
    ('user2', 'user2@example.com', 'a1b2c3d4'),    # Valid case with different characters
])
def test_user_create_model(username, email, password):
    user_create = UserCreate(username=username, email=email, password=password)
    assert user_create.username == username
    assert user_create.email == email
    assert user_create.password == password

@pytest.mark.parametrize("id, username, email", [
    (1, 'user1', 'user1@example.com'),  # Valid case
    (2, 'user2', 'user2@example.com'),  # Valid case with different values
])
def test_user_model_valid(id, username, email):
    user = User(id=id, username=username, email=email)
    assert user.id == id
    assert user.username == username
    assert user.email == email

@pytest.mark.parametrize("id, username, email", [
    ('not_an_int', 'user1', 'user1@example.com'),   # Invalid id (string)
    (3.14, 'user2', 'user2@example.com'),           # Invalid id (float)
    (-1, 'user3', 'user3@example.com'),             # Invalid id (negative integer)
    (0, 'user4', 'user4@example.com'),              # Invalid id (zero, if not allowed)
])
def test_user_model_invalid_id(id, username, email):
    with pytest.raises(ValidationError):
        User(id=id, username=username, email=email)

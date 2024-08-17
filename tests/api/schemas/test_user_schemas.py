import pytest
from pydantic import ValidationError
from app.api.schemas.user_schemas import UserBase, UserCreate, User, TokenResponse, LoginRequest

# Tests for UserBase model
def test_user_base_model_valid():
    user = UserBase(username="SampleUser", email="a@b.com")
    assert user.username == "SampleUser"
    assert user.email == "a@b.com"
    assert user.role == "user"  # Default role value

@pytest.mark.parametrize("username", [
    '@adsfas',      # Contains special character '@'
    'asd adfds',    # Contains a space
    'asdfds. ',     # Contains a period '.' and a space at the end
    'asdf. ',     # Contains a period '.' and a space at the end
    'asdf',     # Contains a period '.' and a space at the end
])
def test_user_base_model_invalid_username(username):
    with pytest.raises(ValidationError) as exc_info:
        UserBase(username=username, email="a@b.com")
    assert "Username must be a single word without spaces, whitespace, or special characters." in str(exc_info.value) or \
        'Username must be at least 5 characters long.' in str(exc_info.value)

@pytest.mark.parametrize("invalid_email", [
    'plainaddress',          # No @ symbol
    'plainaddress.com',      # Website
    '@missingusername.com',  # Missing username
    'username@.com',         # Missing domain name
    'username@com',          # Missing period in domain
    'username@domain..com',  # Double period in domain
])
def test_user_base_model_invalid_email(invalid_email):
    with pytest.raises(ValidationError) as exc_info:
        UserBase(username='username', email=invalid_email)
    assert "value is not a valid email address" in str(exc_info.value)

# Tests for UserCreate model
@pytest.mark.parametrize("username, email, password", [
    ('user1', 'user1@example.com', 'Password1@'),  # Valid case
    ('user2', 'user2@example.com', 'A1b2c3d4@'),    # Valid case with different characters
])
def test_user_create_model(username, email, password):
    user_create = UserCreate(username=username, email=email, password=password)
    assert user_create.username == username
    assert user_create.email == email
    assert user_create.password == password

@pytest.mark.parametrize("password", [
    'short',  # Too short
    'noDigits',  # No digits
    '12345678',  # No letters
    'ASDF123!',  # No letters
    'ASdF1233',  # No letters
])
def test_user_create_model_invalid_password(password):
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(username='user1', email='user@example.com', password=password)
    assert ("String should have at least 8 characters" in str(exc_info.value) or
            "Value error, " in str(exc_info))

# Tests for User model
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

# Tests for TokenResponse model
def test_token_response_valid():
    token_response = TokenResponse(access_token="some_token")
    assert token_response.access_token == "some_token"
    assert token_response.token_type == "bearer"  # Default value

@pytest.mark.parametrize("access_token", [
    '',  # Empty token
    None,  # None token
])
def test_token_response_invalid(access_token):
    with pytest.raises(ValidationError) as exc_info:
        TokenResponse(access_token=access_token)
    assert ("Value error, Access token cannot be empty" in str(exc_info.value) or
            "Input should be a valid string" in str(exc_info.value) or
            "Value error, Access token cannot be empty" in str(exc_info.value))

# Tests for LoginRequest model
def test_login_request_valid():
    login_request = LoginRequest(username="user1", password="Validpassword1!")
    assert login_request.username == "user1"
    assert login_request.password == "Validpassword1!"

@pytest.mark.parametrize("username, password", [
    ('', 'Validpassword0!'),  # Empty username
    ('user', 'Validpassword0!'),  # short username
    ('user1', ''),           # Empty password
    ('user1', 'ivalidpw0!'), # no upper case
    ('user1', 'INVALIDPW0!'),# no lower case
    ('user1', 'IInvalidPW!'),# no int in password
    ('user1', 'IInvalidPW0'),# np special char
    ('user1', 'short'),      # Short password
])
def test_login_request_invalid(username, password):
    with pytest.raises(ValidationError) as exc_info:
        LoginRequest(username=username, password=password)
    assert "String should have at least 8 characters" in str(exc_info.value) or \
            "Value error," in str(exc_info.value)


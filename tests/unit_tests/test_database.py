# test_database.py
import os
import pytest
from unittest.mock import patch, MagicMock
from app.db.database import Database

@pytest.fixture
def mock_database():
    with patch('app.db.database.PostgresqlDatabase') as mock_db:
        yield mock_db

@pytest.fixture
def database_instance(mock_database):
    # Create a Database instance with a mock URL
    db_url = "postgresql://user:password@localhost/dbname"
    return Database(db_url)

def test_connect(mock_database, database_instance):
    # Arrange
    mock_database.return_value.connect = MagicMock()

    # Act
    database_instance.connect()

    # Assert
    mock_database.return_value.connect.assert_called_once()

def test_close(mock_database, database_instance):
    # Arrange
    mock_db_instance = mock_database.return_value
    mock_db_instance.is_closed.return_value = False

    # Act
    database_instance.close()

    # Assert
    mock_db_instance.close.assert_called_once()

def test_create_tables(mock_database, database_instance):
    # Arrange
    mock_db_instance = mock_database.return_value
    mock_models = []  # Add your model classes here

    # Act
    database_instance.create_tables(mock_models)

    # Assert
    mock_db_instance.create_tables.assert_called_once_with(mock_models, safe=True)

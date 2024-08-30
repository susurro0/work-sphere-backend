import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, create_autospec, patch

from app.api.endpoints.text_generator_routes import TextGeneratorRoutes  # Adjust this import based on your app's structure

from app.clients.OllamaClient import OllamaClient

@pytest.fixture
def client_success():
    app = FastAPI()
    # Initialize the TaskRoutes with mocked dependencies
    text_generator_routes = TextGeneratorRoutes(ollama_host="mock_ollama_host")

    app.include_router(text_generator_routes.router)

    return TestClient(app)

@pytest.fixture
def client_exception():
    app = FastAPI()
    # Initialize the TaskRoutes with mocked dependencies
    text_generator_routes = TextGeneratorRoutes(ollama_host="mock_ollama_host")

    app.include_router(text_generator_routes.router)

    return TestClient(app)


def test_generate_text_success(client_success):
    # Define a valid request body
    with(patch.object(OllamaClient, "generate_text", return_value="mocked response")):
        request_body = {"example_text": "Sample example text", "cues": "Sample cues"}

        response = client_success.post("/api/generateText", json=request_body)

        assert response.status_code == 200
        assert response.json() == {"generated_text": "mocked response"}

def test_generate_text_invalid_input(client_exception):
    # Define an invalid request body (missing required fields)
    request_body = {"example_text": "Sample example text"}

    response = client_exception.post("/api/generateText", json=request_body)

    assert response.status_code == 422


def test_generate_text_prompt_creation(client_success):
    with patch("app.clients.prompts.create_report_prompt") as mock_create_report_prompt:
        mock_create_report_prompt.return_value = "mocked prompt"

        request_body = {"example_text": "Sample example text", "cues": "Sample cues"}
        response = client_success.post("/api/generateText", json=request_body)

        # mock_create_report_prompt.assert_called_once_with("Sample example text", "Sample cues")
        assert response.status_code == 200
        assert response.json() == {"generated_text": ""}

@patch("app.clients.OllamaClient.OllamaClient.generate_text")
def test_generate_text_generate_text_failed(mock_generate_text, client_success):
    # Simulate an exception being raised by OllamaClient
    mock_generate_text.side_effect = Exception("Mock OllamaClient error")

    request_body = {"example_text": "Sample example text", "cues": "Sample cues"}
    response = client_success.post("/api/generateText", json=request_body)

    # Verify that the response status code is 500
    assert response.status_code == 500
    assert response.json() == {"detail": "Mock OllamaClient error"}
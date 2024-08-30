import pytest
from pydantic import ValidationError

from app.api.schemas.text_generator_schemas import GenerateTextRequest


# Test valid input
def test_generate_text_request_valid_input():
    # Create an instance of GenerateTextRequest with valid input
    request = GenerateTextRequest(example_text="Sample text", cues="Some cues")
    assert request.example_text == "Sample text"
    assert request.cues == "Some cues"

# Test missing example_text field
def test_generate_text_request_missing_example_text():
    with pytest.raises(ValidationError) as excinfo:
        GenerateTextRequest(cues="Some cues")
    assert "validation error" in str(excinfo.value)

# Test missing cues field
def test_generate_text_request_missing_cues():
    with pytest.raises(ValidationError) as excinfo:
        GenerateTextRequest(example_text="Sample text")
    assert "validation error" in str(excinfo.value)

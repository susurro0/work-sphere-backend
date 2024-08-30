import pytest
from pydantic import ValidationError
from app.api.schemas.pathfinder_schemas import PathfinderRequest, PathfinderResponse

def test_pathfinder_request_valid():
    valid_data = {
        "grid": [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 2]
        ],
        "algorithm": "a-star"
    }

    request = PathfinderRequest(**valid_data)
    assert request.grid == valid_data["grid"]
    assert request.algorithm == valid_data["algorithm"]

def test_pathfinder_request_invalid_algorithm():
    invalid_data = {
        "grid": [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 2]
        ],
        "algorithm": "InvalidAlgorithm"
    }

    with pytest.raises(ValidationError) as excinfo:
        PathfinderRequest(**invalid_data)
    assert "algorithm" in str(excinfo.value)

def test_pathfinder_request_default_algorithm():
    data = {
        "grid": [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 2]
        ]
    }

    request = PathfinderRequest(**data)
    assert request.algorithm == "a-star"

def test_pathfinder_response_with_path():
    data = {
        "path": [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]]
    }

    response = PathfinderResponse(**data)
    assert response.path == data["path"]

def test_pathfinder_response_without_path():
    response = PathfinderResponse()
    assert response.path is None

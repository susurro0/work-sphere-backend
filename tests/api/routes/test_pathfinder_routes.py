import pytest
from fastapi.testclient import TestClient
from app.api.endpoints.pathfinder_routes import PathfinderRoutes

# Instantiate PathfinderRoutes
pathfinder_routes = PathfinderRoutes()
app = pathfinder_routes.router

client = TestClient(app)

def test_a_star_algorithm():
    request_data = {
        "grid": [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 2]
        ],
        "algorithm": "a-star"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    expected_path = [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]]  # Adjust based on expected behavior
    assert data["path"] == expected_path

def test_a_star_algorithm_no_path():
    request_data = {
        "grid": [
            [1, -1, 2],
            [0, -1, 0],
            [0,-1, 0]
        ],
        "algorithm": "a-star"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    assert data["path"] == []  # No path should be found

def test_dijkstra_algorithm():
    request_data = {
        "grid": [
            [1, 0, 0, 0, 0],
            [0, -1, -1, -1, 0],
            [0, -1, 0, -1, 2],
            [0, 0, 0, 0, 0]
        ],
        "algorithm": "dijkstra"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # Adjust the expected path based on the grid and Dijkstra's algorithm behavior
    expected_path = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 4], [2, 4]]  # Example path
    assert data["path"] == expected_path

def test_dijkstra_algorithm_no_path():
    request_data = {
        "grid": [
            [1, -1, -1, -1, 2],
            [0, -1, -1, -1, 0],
            [0, -1, 0, -1, 0],
            [0, 0, 0, 0, -1]
        ],
        "algorithm": "dijkstra"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    assert data["path"] == []  # No path should be found


def test_dfs_simple_path():
    grid = [
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2]
        ]
    request_data = {
        "grid": grid,
        "algorithm": "dfs"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    assert data['path'][-1] == [2, 4]

def test_dfs_with_walls():
    request_data = {
        "grid": [
            [1, 0, 0, 0, 0],
            [0, -1, -1, -1, 0],
            [0, -1, 0, -1, 2],
            [0, 0, 0, 0, 0]
        ],
        "algorithm": "dfs"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # DFS might not always return the shortest path, but it should return a valid path that avoids walls
    expected_path = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 4],
                     [2, 4]]  # This assumes DFS visits the upper row first
    assert data["path"] == expected_path

def test_dfs_no_path():
    request_data = {
        "grid": [
            [1, 0, -1],
            [-1, -1, -1],
            [0, 0, 2]
        ],
        "algorithm": "dfs"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    assert data["path"] == []  # No path should be found because of walls

def test_dfs_with_multiple_routes():
    request_data = {
        "grid": [
            [1, 0, 0, 0, 2],
            [0, -1, -1, -1, 0],
            [0, 0, 0, 0, 0]
        ],
        "algorithm": "dfs"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # There could be multiple valid paths, so we check that one of them is returned
    expected_path_1 = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]
    expected_path_2 = [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4]]

    assert data["path"] in [expected_path_1, expected_path_2]  # DFS might choose either based on stack order

@pytest.mark.parametrize("grid,expected_path", [
    (
            [[1, 0, 0, 2]],
            [[0, 0], [0, 1], [0, 2], [0, 3]]  # Simple horizontal path
    ),
    (
            [[1], [0], [0], [2]],
            [[0, 0], [1, 0], [2, 0], [3, 0]]  # Simple vertical path
    ),
])
def test_dfs_various_scenarios(grid, expected_path):
    request_data = {
        "grid": grid,
        "algorithm": "dfs"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    assert data["path"] == expected_path

def test_bfs_with_walls():
    request_data = {
        "grid": [
            [1, 0, 0, 0, 0],
            [0, -1, -1, -1, 0],
            [0, -1, 0, -1, 2],
            [0, 0, 0, 0, 0]
        ],
        "algorithm": "bfs"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # BFS should return the shortest path
    expected_path = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 4], [2, 4]]
    assert data["path"] == expected_path

def test_bfs_no_path():
    request_data = {
        "grid": [
            [1, -1, 0],
            [-1, -1, -1],
            [0, 0, 2]
        ],
        "algorithm": "bfs"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # No path should be found
    assert data["path"] == []
def test_bfs_open_grid():
    request_data = {
        "grid": [
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 2]
        ],
        "algorithm": "bfs"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # The shortest path in an open grid
    expected_path = [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]]
    assert data["path"] == expected_path


def test_bfs_multiple_equal_paths():
    request_data = {
        "grid": [
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 2]
        ],
        "algorithm": "bfs"
    }

    response = client.post("/api/pathfinder/", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # Multiple shortest paths exist; BFS should return one of them
    expected_paths = [
        [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [2, 3]],
        [[0, 0], [0, 1], [0, 2], [0, 3], [1, 3], [2, 3]]
    ]
    assert data["path"] in expected_paths

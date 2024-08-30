import logging
from fastapi import APIRouter, HTTPException
import heapq
from typing import Tuple, List, Dict

from app.api.schemas.pathfinder_schemas import PathfinderRequest, PathfinderResponse


# PathfinderRoutes class
class PathfinderRoutes:
    def __init__(self):
        self.router = APIRouter()

        @self.router.post("/api/pathfinder/", response_model=PathfinderResponse)
        def find_path(request: PathfinderRequest):
            try:
                # Select the algorithm based on the request
                if request.algorithm == "a-star":
                    path = self.a_star_search(request.grid)
                elif request.algorithm == "dijkstra":
                    path = self.dijkstra_search(request.grid)
                elif  request.algorithm == "dfs":
                    path = self.dfs_search(request.grid)
                elif request.algorithm == "bfs":
                    path = self.bfs_search(request.grid)
                else:
                    raise HTTPException(status_code=400, detail="Algorithm not supported")

                return PathfinderResponse(path=path)
            except Exception as e:
                logging.error(f"Failed to find path: {e}")
                raise HTTPException(status_code=500, detail="An error occurred while finding the path.")

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        # Manhattan distance heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_search(self, grid: List[List[int]]) -> List[List[int]]:
        import heapq

        # Directions for movement (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


        # Find start and end positions
        start = end = None
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 1:
                    start = (i, j)
                elif cell == 2:
                    end = (i, j)

        if not start or not end:
            raise HTTPException(status_code=400, detail="Start or end position not found in the grid.")

        # Priority queue for the open set
        open_set = []
        heapq.heappush(open_set, (0, start))

        # Dictionaries for tracking the cost and path
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}

        while open_set:
            _, current = heapq.heappop(open_set)

            # If the current position is the end, reconstruct and return the path
            if current == end:
                path = []
                while current in came_from:
                    path.append(list(current))
                    current = came_from[current]
                path.append(list(start))
                return path[::-1]  # Return reversed path

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                # Skip invalid or blocked positions
                if (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and
                        grid[neighbor[0]][neighbor[1]] != -1):
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # Return an empty list if no path was found
        return []

    def dijkstra_search(self, grid: List[List[int]]) -> List[List[int]]:

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def reconstruct_path(came_from: Dict[Tuple[int, int], Tuple[int, int]], current: Tuple[int, int]) -> List[
            List[int]]:
            path = []
            while current in came_from:
                path.append(list(current))
                current = came_from[current]
            path.append(list(current))  # Add the start position
            return path[::-1]  # Reverse the path to start from the beginning

        start, end = self.find_start_end(grid)
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while open_set:
            current_cost, current = heapq.heappop(open_set)

            if current == end:
                return reconstruct_path(came_from, current)

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if self.is_valid_position(neighbor, grid):
                    new_cost = current_cost + 1
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        heapq.heappush(open_set, (new_cost, neighbor))
                        came_from[neighbor] = current

        return []

    def find_start_end(self, grid: List[List[int]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        start = end = None
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 1:
                    start = (i, j)
                elif cell == 2:
                    end = (i, j)
        if not start or not end:
            raise HTTPException(status_code=400, detail="Start or end position not found in the grid.")
        return start, end

    def is_valid_position(self, position: Tuple[int, int], grid: List[List[int]]) -> bool:
        return (0 <= position[0] < len(grid) and
                0 <= position[1] < len(grid[0]) and
                grid[position[0]][position[1]] != -1)

    def dfs_search(self, grid: List[List[int]]) -> List[List[int]]:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        start, end = self.find_start_end(grid)
        stack = [(start, [start])]
        visited = set()

        while stack:
            current, path = stack.pop()

            if current == end:
                return [list(p) for p in path]

            if current in visited:
                continue

            visited.add(current)

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if self.is_valid_position(neighbor, grid) and neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

        return []

    def bfs_search(self, grid: List[List[int]]) -> List[List[int]]:
        from collections import deque

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        start, end = self.find_start_end(grid)
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            current, path = queue.popleft()

            if current == end:
                return [list(p) for p in path]

            if current in visited:
                continue

            visited.add(current)

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if self.is_valid_position(neighbor, grid) and neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return []

    # def bidirectional_search(self, grid: List[List[str]]) -> List[List[int]]:
    #     from collections import deque
    #     start, end = self.find_start_end(grid)
    #     if start == end:
    #         return [list(start)]
    #
    #     start_front = {start: None}
    #     end_front = {end: None}
    #     start_queue = deque([start])
    #     end_queue = deque([end])
    #
    #     while start_queue and end_queue:
    #         if start_queue:
    #             current = start_queue.popleft()
    #             for neighbor in self.get_neighbors(current, grid):
    #                 if neighbor in end_front:
    #                     return self.reconstruct_bidirectional_path(start_front, end_front, neighbor)
    #                 if neighbor not in start_front:
    #                     start_queue.append(neighbor)
    #                     start_front[neighbor] = current
    #
    #         if end_queue:
    #             current = end_queue.popleft()
    #             for neighbor in self.get_neighbors(current, grid):
    #                 if neighbor in start_front:
    #                     return self.reconstruct_bidirectional_path(start_front, end_front, neighbor)
    #                 if neighbor not in end_front:
    #                     end_queue.append(neighbor)
    #                     end_front[neighbor] = current
    #
    #     return []
    #
    # def greedy_best_first_search(self, grid: List[List[str]]) -> List[List[int]]:
    #     import heapq
    #     start, end = self.find_start_end(grid)
    #     open_set = []
    #     heapq.heappush(open_set, (0, start))
    #     came_from = {}
    #     while open_set:
    #         _, current = heapq.heappop(open_set)
    #         if current == end:
    #             return self.reconstruct_path(came_from, current)
    #         for neighbor in self.get_neighbors(current, grid):
    #             if neighbor not in came_from:
    #                 heapq.heappush(open_set, (self.heuristic(neighbor, end), neighbor))
    #                 came_from[neighbor] = current
    #     return []
    #
    # def jump_point_search(self, grid: List[List[str]]) -> List[List[int]]:
    #     from heapq import heappush, heappop
    #     start, end = self.find_start_end(grid)
    #     open_set = []
    #     heappush(open_set, (0, start))
    #     came_from = {}
    #     g_score = {start: 0}
    #     while open_set:
    #         _, current = heappop(open_set)
    #         if current == end:
    #             return self.reconstruct_path(came_from, current)
    #         for neighbor in self.jump_neighbors(current, end, grid):
    #             tentative_g_score = g_score[current] + self.distance(current, neighbor)
    #

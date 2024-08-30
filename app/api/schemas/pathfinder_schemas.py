from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class PathfinderRequest(BaseModel):
    grid: List[List[int]]
    algorithm: Literal["a-star", "dijkstra", "dfs", "bfs"] = "a-star"

# Define the response schema
class PathfinderResponse(BaseModel):
    path: Optional[List[List[int]]] = Field(None, description="List of coordinates representing the path")

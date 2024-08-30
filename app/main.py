import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.endpoints import TaskRoutes, UserRoutes, PathfinderRoutes, TextGeneratorRoutes
from .core.initializer import AppInitializer
from .db.database import database_instance
from .dependencies import Dependency


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Adjust to your frontend URL
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

    # Initialize application components
    initializer = AppInitializer(app, database_instance.database)
    initializer.initialize()

    dependency = Dependency(initializer.db)
    # Include routers
    task_routes = TaskRoutes(dependency = dependency)
    user_routes = UserRoutes(dependency = dependency)
    pathfinder_routes = PathfinderRoutes()
    text_generator_routes = TextGeneratorRoutes(ollama_host=os.getenv('OLLAMA_HOST'))
    app.include_router(task_routes.router)
    app.include_router(user_routes.router)
    app.include_router(pathfinder_routes.router)
    app.include_router(text_generator_routes.router)



    return app


# Create the FastAPI app instance
app = create_app()


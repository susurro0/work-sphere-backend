from fastapi import FastAPI

from .api.endpoints import TaskRoutes
from .core.initializer import AppInitializer
from .db.database import database_instance
from .dependencies import Dependency


def create_app() -> FastAPI:
    app = FastAPI()

    # Initialize application components
    initializer = AppInitializer(app, database_instance.database)
    initializer.initialize()

    dependency = Dependency(initializer.db)
    # Include routers
    task_routes = TaskRoutes(dependency = dependency)
    app.include_router(task_routes.router)

    return app


# Create the FastAPI app instance
app = create_app()

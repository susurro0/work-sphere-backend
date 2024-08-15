from app.db.database import database_instance
from app.models.task_models import Task

class AppInitializer:
    def __init__(self, app, db):
        self.app = app
        self.db = db

    def initialize(self):
        self.app.state.db = self.db
        self.db.create_tables([Task])  # Create your models here
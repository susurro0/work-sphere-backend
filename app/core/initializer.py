from app.db.database import database_instance
from app.models.task_models import Task
from app.models.user_models import User


class AppInitializer:
    def __init__(self, app, db):
        self.app = app
        self.db = db

    def initialize(self):
        self.app.state.db = self.db
        self.db.create_tables([Task, User])  # Create your models here
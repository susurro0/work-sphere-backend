from app.db.database import Database
from app.utils.auth_service import AuthService


class Dependency:
    def __init__(self, db: Database ):
        self.db = db

    def get_db(self):
        try:
            self.db.connect()
            yield self.db.database
        finally:
            self.db.close()

    def get_auth_service(self):
        return AuthService(self.db)
from argon2 import PasswordHasher
from peewee import Model, IntegerField, CharField, DateTimeField, fn
from app.db.database import database_instance

# Initialize Argon2 password hasher
ph = PasswordHasher()

class User(Model):
    id = IntegerField(primary_key=True)
    username = CharField(unique=True, max_length=50)
    email = CharField(unique=True, max_length=100)
    password = CharField(max_length=100)  # Store hashed password
    created_at = DateTimeField(default=fn.now)
    role = CharField(default="user")

    class Meta:
        database = database_instance.database  # Set the database attribute
        table_name = 'users'

    def set_password(self, plain_password):
        self.password = ph.hash(plain_password)  # Hash password with Argon2

    def verify_password(self, plain_password):
        # Verify password against the hashed password
        ph.verify(self.password, plain_password)
        return True

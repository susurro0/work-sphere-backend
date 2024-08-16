from peewee import Model, IntegerField, CharField, TextField, DateTimeField, fn

from app.db.database import database_instance


class User(Model):
    id = IntegerField(primary_key=True)
    username = CharField(unique=True, max_length=50)
    email = CharField(unique=True, max_length=100)
    password = CharField(max_length=100)
    created_at = DateTimeField(default=fn.now)
    role = CharField(default='user')

    class Meta:
        database = database_instance.database  # Set the database attribute
        table_name = 'users'
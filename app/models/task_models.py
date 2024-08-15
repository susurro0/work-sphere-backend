from peewee import Model, IntegerField, CharField, TextField, DateTimeField, fn

from app.db.database import database_instance


class Task(Model):
    id = IntegerField(primary_key=True)
    title = CharField(index=True)
    description = TextField(null=True)
    status = TextField(null=False)  # Add completed status
    created_at = DateTimeField(default=fn.now)

    class Meta:
        database = database_instance.database  # Set the database attribute
        table_name = 'tasks'
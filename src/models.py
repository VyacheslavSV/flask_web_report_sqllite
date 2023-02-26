from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, TimeField

db = SqliteDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Driver(BaseModel):
    abbr = CharField(unique=True)
    name = CharField()
    team = CharField()

    class Meta:
        db_table = 'drivers'


class StartLog(BaseModel):
    driver = ForeignKeyField(Driver, backref='start_logs')
    time_start = TimeField(null=True)

    class Meta:
        db_table = 'start_logs'


class EndLog(BaseModel):
    driver = ForeignKeyField(Driver, backref='end_logs')
    time_finish = TimeField(null=True)

    class Meta:
        db_table = 'end_logs'

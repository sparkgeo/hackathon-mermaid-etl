import databases
import sqlalchemy

from . import settings

engine = sqlalchemy.create_engine(settings.POSTGRES_URL)
db = databases.Database(settings.POSTGRES_URL)
metadata = sqlalchemy.MetaData()
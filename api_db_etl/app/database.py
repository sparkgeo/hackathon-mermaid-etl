import databases
import sqlalchemy

from app.settings import POSTGRES_URL

engine = sqlalchemy.create_engine(POSTGRES_URL)
db = databases.Database(POSTGRES_URL)
metadata = sqlalchemy.MetaData()

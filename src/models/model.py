from orator import DatabaseManager, Model
from config.settings import DATABASES

db = DatabaseManager(DATABASES)
Model.set_connection_resolver(db)

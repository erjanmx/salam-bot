from orator import DatabaseManager, Model
from config.database import databases

db = DatabaseManager(databases)
Model.set_connection_resolver(db)

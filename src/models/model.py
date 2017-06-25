from config.settings import DATABASES
from orator import DatabaseManager, Model

db = DatabaseManager(DATABASES)
Model.set_connection_resolver(db)

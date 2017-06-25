import os
from dotenv import load_dotenv


env_file = '.env'
if os.path.isfile(env_file):
    load_dotenv(env_file)

DEBUG = os.getenv('APP_DEBUG', False)
SALAM_BOT_TOKEN_KEY = os.getenv('APP_TOKEN_KEY')
SALAM_BOT_TOKEN_VALUE = os.getenv('APP_TOKEN_VALUE')
NAMBA_ONE_API_TOKEN = os.getenv('NAMBA_ONE_API_TOKEN')

DATABASES = {
    'mysql': {
        'driver': 'mysql',
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'database': os.getenv('DB_NAME'),
        'password': os.getenv('DB_PASSWORD'),
        'prefix': ''
    }
}

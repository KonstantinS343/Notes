from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.environ.get('HOST')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
PORT = os.environ.get('PORT')
POSTGRES_DB_TEST = os.environ.get('POSTGRES_DB_TEST')

DB_URL = os.environ.get('DB_URL')
TEST_DB_URL = os.environ.get('TEST_DB_URL')

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

SECRET = os.environ.get("SECRET")

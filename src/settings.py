from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.environ.get('HOST')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
PORT = os.environ.get('PORT')
DB_TEST_NAME = os.environ.get('DB_TEST_NAME')

DB_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{POSTGRES_DB}'

TEST_DB_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{DB_TEST_NAME}'

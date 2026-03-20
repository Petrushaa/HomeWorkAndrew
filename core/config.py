import os

DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/app_db")

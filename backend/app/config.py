import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")

    JWT_SECRET = os.getenv("JWT_SECRET", "change_this_secret")
    JWT_ALG = os.getenv("JWT_ALG", "HS256")
    JWT_EXPIRE_DAYS = int(os.getenv("JWT_EXPIRE_DAYS", "7"))

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "perspectiveconnect")

    AUDIO_STORAGE_DIR = os.getenv("AUDIO_STORAGE_DIR", "./storage")

settings = Settings()


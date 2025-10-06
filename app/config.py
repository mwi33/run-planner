import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-this")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///instance/app.db")

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/appdb"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True  # CI + localhost
    SESSION_COOKIE_SAMESITE = "Lax"

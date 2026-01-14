import os
 
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    # Connection string for PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/postgres")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
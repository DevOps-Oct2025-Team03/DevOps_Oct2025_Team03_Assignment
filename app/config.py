# Stores application configuration (secret keys), reads environment variables

import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

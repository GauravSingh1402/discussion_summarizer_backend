import os
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET = os.environ.get("JWT_SECRET")
class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET = os.environ.get("JWT_SECRET")
class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET = os.environ.get("JWT_SECRET")
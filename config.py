import os

class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_SECRET_KEY = 'andela13'
    DATABASE_URI = os.getenv('DATABASE_URL')
    

class DevelopmentConfig(Config):
    DEBUG=True
    ENV = 'development'
    DATABASE_URI = 'postgresql://localhost/store_db'
    TESTING = False


class TestingConfig(Config):
    DEBUG=True
    ENV = 'testing'
    DATABASE_URI= 'postgresql://localhost/test_db'
    TESTING = True

app_configuration = {
    "development":DevelopmentConfig,
    "testing":TestingConfig
}


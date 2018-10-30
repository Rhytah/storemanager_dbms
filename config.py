class Config:
    DEBUG = False
    TESTING = False
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'



class DevelopmentConfig(Config):
    DEBUG=True
    ENV = 'development'
    DATABASE = 'store_db'
    TESTING = False


class TestingConfig(Config):
    DEBUG=True
    ENV = 'testing'
    DATABASE = 'store_test'
    TESTING = True

app_configuration = {
    "development":DevelopmentConfig,
    "testing":TestingConfig
}


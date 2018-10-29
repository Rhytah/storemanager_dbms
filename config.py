class Config:
    DEBUG=False


class DevelopmentConfig(Config):
    DEBUG=True

class TestingConfig(Config):
    DEBUG=True

app_configuration = {
    "development":DevelopmentConfig,
    "testing":TestingConfig
}
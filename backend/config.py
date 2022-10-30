import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = "8080"

class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    PORT = "8080"

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
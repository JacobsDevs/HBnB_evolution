import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://jacob:jacob@172.17.0.2/hbnb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://jacob:jacob@172.17.0.2/hbnb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'testing': TestingConfig
}

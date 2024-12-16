SECRET_KEY = 'secret_key_sdsfs'

SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    WTF_CSRF_ENABLED = True
    TESTING = False
    SECRET_KEY = 'secret_key_sdsfs'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "instance\\test-db.sqlite")
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')

config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig,
    'test': TestingConfig
}
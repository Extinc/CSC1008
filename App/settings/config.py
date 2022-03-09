class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQL_ECHO = False
    MAP_SRID = 4326


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///settings/db2.sqlite'
    EXTENSION_URL = "./addon/mod_spatialite.dylib"
    DEBUG = True
    FLASK_ENV = 'development'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///settings/db2.sqlite'
    EXTENSION_URL = "./addon/mod_spatialite.dylib"
    DEBUG = False
    FLASK_ENV = 'production'


config_ = {
    'default': DevConfig,
    'dev': DevConfig,
    'prod': ProdConfig
}
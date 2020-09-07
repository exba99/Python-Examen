import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_CONFIG = 'development'

    @staticmethod
    def init_app(app): 
        pass

class DevelopmentConfig(Config): 
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://root:@localhost/py_cadastre'

class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or 'mysql+pymysql://root:@localhost/py_cadastre'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
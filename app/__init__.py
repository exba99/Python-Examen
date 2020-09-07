from flask import Flask, render_template 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from config import config
from flask_login import LoginManager



login_manager = LoginManager()
login_manager.login_view = 'admin.adminLog'


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__) 
    
    login_manager.init_app(app)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from app.terrain import terrain as terrain_blueprint
    from app.admin import admin as admin_blueprint 
    app.register_blueprint(terrain_blueprint)
    app.register_blueprint(admin_blueprint)




    return app
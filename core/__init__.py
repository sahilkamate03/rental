# from cryptography.fernet import Fernet
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


from core.common.variables import (
    DB_NAME,
    DB_PWD,
    DB_SERVER,
    DB_USER,
    SQL_ACLCHEMY_KEY,
)

login_manager = LoginManager()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SECRET_KEY"] = SQL_ACLCHEMY_KEY

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{DB_USER}:{DB_PWD}@{DB_SERVER}/{DB_NAME}"
    )
    db.init_app(app)
    login_manager.init_app(app)
    from core.api import dashboard, home, property, profile

    app.register_blueprint(home.home)
    app.register_blueprint(dashboard.dashboard)
    app.register_blueprint(property.property)
    app.register_blueprint(profile.profile)

    return app

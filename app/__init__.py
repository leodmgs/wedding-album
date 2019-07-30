from flask import Flask
from flask_bootstrap import Bootstrap
from flask_session import Session
from app.main.database import DB
from app.config import SECRET_KEY


def create_app(config):
    app = Flask(__name__)
    session = Session()
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config.from_object("app.config")
    session.init_app(app)
    DB.init()
    Bootstrap(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)


from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import config_settings
from app.controllers.admin.views import admin_bp
from app.controllers.mentor.views import mentor_bp

migrate = Migrate()
db = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(config_settings['development'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()
    app.register_blueprint(admin_bp)
    app.register_blueprint(mentor_bp)
    return app
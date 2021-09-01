from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import config_settings
from app.controllers.admin.views import admin_bp
from app.controllers.mentor.views import mentor_bp
from app.controllers.landing.views import landing_bp
migrate = Migrate()
db = None

def create_app():
    global app, db
    app = Flask(__name__)
    app.config.from_object(config_settings['development'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    from app.models import Matches, MentorResponses, TeamResponses
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()
    app.register_blueprint(admin_bp)
    app.register_blueprint(mentor_bp)
    app.register_blueprint(landing_bp)
    return app
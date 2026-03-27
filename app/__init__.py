from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from app.extensions import db, login_manager
from app.models import User

csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.blueprints.main import main_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.patient import patient_bp
    from app.blueprints.college import college_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(patient_bp, url_prefix="/patient")
    app.register_blueprint(college_bp, url_prefix="/college")

    # Create tables
    with app.app_context():
        db.create_all()

    # Register CLI commands
    from app.seed import register_seed_command
    register_seed_command(app)

    return app

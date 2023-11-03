from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import parts of our application
    from app.modules.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # You can add more blueprints here
    # from app.modules.project import project as project_blueprint
    # app.register_blueprint(project_blueprint)

    return app

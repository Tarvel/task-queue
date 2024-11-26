from flask import Flask
from flask_migrate import Migrate
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .utils import make_celery




db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)    
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    celery = make_celery(app)
    celery.set_default()

        

    from app.route import auth, tasks
    app.register_blueprint(auth.auth)
    app.register_blueprint(tasks.task)

    return app, celery


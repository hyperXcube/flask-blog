from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_json('config.json')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .errors.handlers import bp as errors
    from .main.routes import bp as main
    from .posts.routes import bp as posts
    from .users.routes import bp as users

    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)

    return app
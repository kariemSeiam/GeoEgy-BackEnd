# Import necessary modules
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Initialize SQLAlchemy extension
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)





    # Import blueprints and register them
    from .controllers.order_controller import bp as order_bp
    from .controllers.place_controller import bp as place_bp
    from .controllers.user_controller import bp as user_bp

    app.register_blueprint(order_bp, url_prefix='/order')
    app.register_blueprint(place_bp, url_prefix='/place')
    app.register_blueprint(user_bp, url_prefix='/user')

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    
    # Check if the database file exists; if not, create it
    if not os.path.exists(os.path.join(app.root_path, 'data', 'echo.db')):
        with app.app_context():
            db.create_all()




    return app

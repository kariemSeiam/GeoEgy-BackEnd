import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flasgger import Swagger
from flask_cors import CORS
from dotenv import load_dotenv
from loguru import logger
from .config import Config
from .utils.security import handle_unauthorized
from .utils.validators import ValidationError

db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

talisman = Talisman()
swagger = Swagger()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    load_dotenv()
    app.config.from_object(Config)
    CORS(app)

    # Ensure the database directory exists
    db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace('sqlite:///', '')
    db_dir = os.path.dirname(db_path)

    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        logger.info(f"Created database directory at: {db_dir}")

    # Ensure the database file exists
    if not os.path.exists(db_path):
        open(db_path, 'w').close()
        logger.info(f"Created empty database file at: {db_path}")

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    talisman.init_app(app)
    swagger.init_app(app)
    migrate.init_app(app, db)

    # Setup logging
    logger.add("logs/app.log", rotation="1 MB")

    # Register blueprints
    from .controllers.user_controller import bp as user_bp
    from .controllers.order_controller import bp as order_bp
    from .controllers.admin_controller import bp as admin_bp
    from .controllers.search_controller import bp as search_bp
    from .controllers.main_controller import bp as main_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(main_bp)

    # Error handlers
    @app.errorhandler(Exception)
    def handle_exception(e):
        code = 500
        message = 'Internal Server Error'
        if isinstance(e, ValidationError):
            code = 400
            message = str(e)
        elif hasattr(e, 'code'):
            code = e.code
            message = e
        logger.error(f"Error: {e}")
        return jsonify({'code': code, 'message': message, 'data': {}}), code

    @jwt.expired_token_loader
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def expired_token_callback(callback):
        return handle_unauthorized()

    # Ensure all database tables are created
    with app.app_context():
        db.create_all()

    return app

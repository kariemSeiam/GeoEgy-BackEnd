from flask import Blueprint

# Import your controllers here using relative import
from .controllers.admin_controller import bp as admin_bp
from .controllers.order_controller import bp as order_bp
from .controllers.place_controller import bp as place_bp
from .controllers.user_controller import bp as user_bp

# Define blueprints
admin_routes = Blueprint('admin', __name__)
order_routes = Blueprint('order', __name__)
place_routes = Blueprint('place', __name__)
user_routes = Blueprint('user', __name__)

# Register blueprints with their respective URLs
admin_routes.register_blueprint(admin_bp, url_prefix='/admin')
order_routes.register_blueprint(order_bp, url_prefix='/order')
place_routes.register_blueprint(place_bp, url_prefix='/place')
user_routes.register_blueprint(user_bp, url_prefix='/user')

# Export the blueprints if needed
__all__ = ['admin_routes', 'order_routes', 'place_routes', 'user_routes']

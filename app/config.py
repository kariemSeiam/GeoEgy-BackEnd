import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(BASE_DIR, 'data', 'echo.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    SWAGGER = {
        'title': 'GeoEgy API',
        'uiversion': 3
    }
    WHATSAPP_API_URL = os.getenv('WHATSAPP_API_URL')
    WHATSAPP_API_KEY = os.getenv('WHATSAPP_API_KEY')
    RATELIMIT_STORAGE_URL = "redis://localhost:6379/"

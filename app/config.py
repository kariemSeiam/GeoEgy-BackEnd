import os

class Config:
    SECRET_KEY = 'Kkemokoko'
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'echo.db')
    print(f"Database path: {db_path}")  # Added print statement
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_MAX_OVERFLOW = 5

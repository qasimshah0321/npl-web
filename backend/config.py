import os
from datetime import timedelta

class Config:
    """Application configuration"""

    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cricket-tournament-secret-key-change-in-production'

    # Database configuration
    DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'cricket.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'

    # Upload configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    TEAM_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'teams')
    PLAYER_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'players')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # CORS configuration
    CORS_HEADERS = 'Content-Type'

    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        # Ensure upload directories exist
        os.makedirs(Config.TEAM_UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.PLAYER_UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)

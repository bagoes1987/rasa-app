import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    # Base directory
    BASE_DIR = Path(__file__).parent.absolute()
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration - flexible for local and production
    # Priority: Environment variable > Default instance path
    if os.environ.get('FLASK_ENV') == 'production' or os.environ.get('RAILWAY_ENVIRONMENT'):
        # For Railway/production: use /tmp directory
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_PATH') or 'sqlite:////tmp/rasa.db'
    else:
        # For local development: use instance directory
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_PATH') or f'sqlite:///{BASE_DIR}/instance/rasa.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLite optimization for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before using
        'pool_recycle': 3600,   # Recycle connections every hour
    }
    
    # OpenRouter API configuration
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'
    
    # Session configuration
    SESSION_COOKIE_SECURE = True if os.environ.get('FLASK_ENV') == 'production' else False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # File upload configuration (for future use)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size



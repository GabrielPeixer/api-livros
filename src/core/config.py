import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration."""

    # Base Paths
    BASE_DIR = Path(__file__).resolve().parents[2]
    DATA_FOLDER = BASE_DIR / 'data'
    CSV_FILE = DATA_FOLDER / 'books.csv'

    # Scraping Settings
    SITE_URL = os.getenv('SITE_URL', 'https://books.toscrape.com/')

    # API Settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', 25))

    # License & Activation
    PARTIAL_LICENSE_ENABLED = os.getenv(
        'PARTIAL_LICENSE_ENABLED', 'true'
    ).lower() == 'true'
    PARTIAL_LICENSE_SCOPE = os.getenv(
        'PARTIAL_LICENSE_SCOPE', 'scraping-only'
    )
    ACTIVATION_KEY = os.getenv('ACTIVATION_KEY')  # Should be set in env
    if not ACTIVATION_KEY:
        # Fallback for development only
        ACTIVATION_KEY = 'BOOKS-API-DEV-KEY'

    # Performance
    LOW_MEMORY_TARGET_MB = int(os.getenv('LOW_MEMORY_TARGET_MB', '128'))

    # Flask Settings
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        SECRET_KEY = 'dev-secret-key-change-in-production'

    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

    # Database Settings
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///books.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cache Settings
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))


# Expose settings as module-level variables for backward compatibility
# if needed, but prefer using Config class.
# For now, we map them to keep existing code working until fully refactored.
SITE_URL = Config.SITE_URL
DATA_FOLDER = str(Config.DATA_FOLDER)
CSV_FILE = str(Config.CSV_FILE)
API_HOST = Config.API_HOST
API_PORT = Config.API_PORT
ITEMS_PER_PAGE = Config.ITEMS_PER_PAGE
PARTIAL_LICENSE_ENABLED = Config.PARTIAL_LICENSE_ENABLED
PARTIAL_LICENSE_SCOPE = Config.PARTIAL_LICENSE_SCOPE
ACTIVATION_KEY = Config.ACTIVATION_KEY
LOW_MEMORY_TARGET_MB = Config.LOW_MEMORY_TARGET_MB
SECRET_KEY = Config.SECRET_KEY
DEBUG = Config.DEBUG
SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = Config.SQLALCHEMY_TRACK_MODIFICATIONS
CACHE_TYPE = Config.CACHE_TYPE
CACHE_DEFAULT_TIMEOUT = Config.CACHE_DEFAULT_TIMEOUT

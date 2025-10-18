#!/usr/bin/env python
"""
WSGI entry point for production deployment
Compatible with Gunicorn, uWSGI, and Passenger
"""

import os
import sys
from pathlib import Path

# Add the application directory to Python path
app_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(app_dir))

# Ensure we're in production mode
os.environ.setdefault('FLASK_ENV', 'production')

# Import the Flask app
from app import app as application

# For Gunicorn compatibility
app = application

if __name__ == "__main__":
    application.run()


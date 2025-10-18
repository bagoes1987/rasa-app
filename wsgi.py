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
from app import app as application, db

# Initialize database tables for production
with application.app_context():
    db.create_all()
    print("[INIT] Database initialized for production!")

# For Gunicorn compatibility
app = application

if __name__ == "__main__":
    application.run()


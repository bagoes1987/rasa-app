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
from models import Admin

# Initialize database tables for production
with application.app_context():
    db.create_all()
    print("[INIT] Database initialized for production!")
    
    # Create default admin user if not exists
    existing_admin = Admin.query.filter_by(username='admin').first()
    if not existing_admin:
        admin = Admin(
            username='admin',
            nama_lengkap='Administrator RASA',
            email='admin@rasa.sman1belitang.sch.id',
            role='super_admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("[INIT] Default admin user created!")
        print("[INIT] Username: admin, Password: admin123")
    else:
        print("[INIT] Admin user already exists!")

# For Gunicorn compatibility
app = application

if __name__ == "__main__":
    application.run()


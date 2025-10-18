#!/usr/bin/env python
"""
Script to create admin user specifically for Railway deployment
"""

import os
import sys

# Set environment to production for Railway
os.environ['FLASK_ENV'] = 'production'

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app import app, db
from models import Admin

def create_admin_railway():
    """Create admin user for Railway"""
    with app.app_context():
        try:
            # Check if admin already exists
            existing_admin = Admin.query.filter_by(username='admin').first()
            if existing_admin:
                print("✅ Admin user already exists!")
                print(f"Username: {existing_admin.username}")
                print(f"Name: {existing_admin.nama_lengkap}")
                print(f"Email: {existing_admin.email}")
                return
            
            # Create admin user
            admin = Admin(
                username='admin',
                nama_lengkap='Administrator RASA',
                email='admin@rasa.sman1belitang.sch.id',
                role='super_admin'
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Admin user created successfully!")
            print("="*50)
            print("ADMIN CREDENTIALS:")
            print("="*50)
            print("Username: admin")
            print("Password: admin123")
            print("Name: Administrator RASA")
            print("Email: admin@rasa.sman1belitang.sch.id")
            print("Role: super_admin")
            print("="*50)
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating admin: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_admin_railway()

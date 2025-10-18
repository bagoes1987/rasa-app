#!/usr/bin/env python
"""
Script to create default admin user for RASA system
"""

import os
import sys
from app import app, db
from models import Admin

def create_admin():
    """Create default admin user"""
    with app.app_context():
        # Check if admin already exists
        existing_admin = Admin.query.filter_by(username='admin').first()
        if existing_admin:
            print("Admin user already exists!")
            print(f"Username: {existing_admin.username}")
            print(f"Name: {existing_admin.nama_lengkap}")
            print(f"Email: {existing_admin.email}")
            return
        
        # Create default admin
        admin = Admin(
            username='admin',
            nama_lengkap='Administrator RASA',
            email='admin@rasa.sman1belitang.sch.id',
            role='super_admin'
        )
        admin.set_password('admin123')  # Default password
        
        try:
            db.session.add(admin)
            db.session.commit()
            print("[OK] Admin user created successfully!")
            print("="*50)
            print("ADMIN CREDENTIALS:")
            print("="*50)
            print(f"Username: admin")
            print(f"Password: admin123")
            print(f"Name: {admin.nama_lengkap}")
            print(f"Email: {admin.email}")
            print(f"Role: {admin.role}")
            print("="*50)
            print("[WARNING] IMPORTANT: Please change the default password after first login!")
            print("="*50)
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Error creating admin: {e}")

if __name__ == '__main__':
    create_admin()

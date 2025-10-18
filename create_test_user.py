#!/usr/bin/env python
"""
Script to create test user in Railway database
"""

import os
import sys
from datetime import datetime

# Set environment to production for Railway
os.environ['FLASK_ENV'] = 'production'

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app import app, db
from models import User

def create_test_user():
    """Create test user in Railway database"""
    with app.app_context():
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email='septianaramadhani7877@gmail.com').first()
            if existing_user:
                print("✅ User already exists:")
                print(f"   ID: {existing_user.id}")
                print(f"   Nama: {existing_user.nama_lengkap}")
                print(f"   Email: {existing_user.email}")
                print(f"   Password Plain: {existing_user.password_plain}")
                print(f"   Password Check: {existing_user.check_password('123456')}")
                return
            
            # Create new user
            user = User(
                nama_lengkap='Septiana Ramadhani',
                email='septianaramadhani7877@gmail.com',
                nis='2024001',
                tempat_lahir='Jakarta',
                tanggal_lahir=datetime(2006, 1, 1).date(),
                kelas='X'
            )
            user.set_password('123456')
            
            db.session.add(user)
            db.session.commit()
            
            print("✅ Test user created successfully:")
            print(f"   ID: {user.id}")
            print(f"   Nama: {user.nama_lengkap}")
            print(f"   Email: {user.email}")
            print(f"   NIS: {user.nis}")
            print(f"   Password: 123456")
            print(f"   Password Check: {user.check_password('123456')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_test_user()

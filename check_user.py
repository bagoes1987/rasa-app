#!/usr/bin/env python
"""
Script to check user data in database
"""

import os
import sys

# Set environment to production for Railway
os.environ['FLASK_ENV'] = 'production'

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app import app, db
from models import User

def check_user():
    """Check user data in database"""
    with app.app_context():
        try:
            # Check if user exists
            user = User.query.filter_by(email='septianaramadhani7877@gmail.com').first()
            if user:
                print("✅ User found:")
                print(f"   ID: {user.id}")
                print(f"   Nama: {user.nama_lengkap}")
                print(f"   Email: {user.email}")
                print(f"   NIS: {user.nis}")
                print(f"   Password Hash: {user.password_hash[:50]}...")
                print(f"   Password Plain: {user.password_plain}")
                print(f"   Created: {user.created_at}")
                
                # Test password
                print(f"   Password '123456' check: {user.check_password('123456')}")
                print(f"   Password '123456789' check: {user.check_password('123456789')}")
            else:
                print("❌ User not found!")
                
            # List all users
            print("\n📋 All users in database:")
            users = User.query.all()
            for u in users:
                print(f"   - {u.email} ({u.nama_lengkap})")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    check_user()

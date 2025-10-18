#!/usr/bin/env python
"""
RASA - Refleksi dan Asistensi Sosial Emosional Siswa
Quick start script for development
"""

import os
from app import app, db

def init_database():
    """Initialize database if it doesn't exist"""
    with app.app_context():
        db.create_all()
        print("[OK] Database initialized successfully!")

if __name__ == '__main__':
    # Check if .env exists
    if not os.path.exists('.env'):
        print("[WARNING] .env file not found!")
        print("Please create .env file with required configuration.")
        print("See .env.example for reference.\n")
    
    # Initialize database
    if not os.path.exists('rasa.db'):
        print("[INIT] Initializing database...")
        init_database()
    
    # Run the application
    print("\n" + "="*50)
    print("RASA - Starting Application")
    print("="*50)
    print(f"URL: http://localhost:5000")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print("="*50 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)


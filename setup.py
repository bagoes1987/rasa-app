#!/usr/bin/env python
"""
RASA Setup Script
Automatically setup the application for first-time use
"""

import os
import sys
import secrets
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping...")
        return
    
    print("📝 Creating .env file...")
    
    # Generate a secure secret key
    secret_key = secrets.token_hex(32)
    
    # Get OpenRouter API Key from user
    print("\n🔑 OpenRouter API Key Setup:")
    print("   Get your API key from: https://openrouter.ai/")
    api_key = input("   Enter your OpenRouter API Key (or press Enter to skip): ").strip()
    
    if not api_key:
        api_key = "<YOUR_OPENROUTER_API_KEY>"
        print("   ⚠️  You'll need to add the API key later in .env file")
    
    # Create .env content
    env_content = f"""SECRET_KEY={secret_key}
OPENROUTER_API_KEY={api_key}
DATABASE_PATH=sqlite:///rasa.db
FLASK_ENV=development
"""
    
    env_file.write_text(env_content)
    print("✅ .env file created successfully!")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    print("   This may take a few minutes...")
    
    os.system(f"{sys.executable} -m pip install --upgrade pip")
    os.system(f"{sys.executable} -m pip install -r requirements.txt")
    
    print("✅ Dependencies installed!")

def initialize_database():
    """Initialize the database"""
    print("\n🗄️  Initializing database...")
    
    try:
        from app import app, db
        
        with app.app_context():
            db.create_all()
        
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        print("   You can initialize it manually later by running:")
        print("   python run.py")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ['reports']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    print("✅ All directories created!")

def print_next_steps():
    """Print next steps for user"""
    print_header("✅ Setup Complete!")
    
    print("📚 Next Steps:")
    print("\n1️⃣  Start the application:")
    print("   python run.py")
    print("\n2️⃣  Open your browser and visit:")
    print("   http://localhost:5000")
    print("\n3️⃣  Register a new account and start exploring!")
    
    print("\n📖 Documentation:")
    print("   • Quick Start: QUICK_START.md")
    print("   • Full Guide: README.md")
    print("   • Deployment: DEPLOYMENT_GUIDE.md")
    
    if "<YOUR_OPENROUTER_API_KEY>" in Path('.env').read_text():
        print("\n⚠️  IMPORTANT:")
        print("   Don't forget to add your OpenRouter API Key to .env file!")
        print("   Get it from: https://openrouter.ai/")
    
    print("\n💜 Thank you for using RASA!")
    print("="*60 + "\n")

def main():
    """Main setup function"""
    print_header("🌟 RASA Setup Wizard")
    
    try:
        # Check Python version
        check_python_version()
        
        # Create .env file
        create_env_file()
        
        # Ask if user wants to install dependencies
        install = input("\n📦 Install dependencies now? (y/n): ").lower()
        if install == 'y':
            install_dependencies()
        else:
            print("⚠️  Skipping dependency installation.")
            print("   Run 'pip install -r requirements.txt' manually later.")
        
        # Create directories
        create_directories()
        
        # Ask if user wants to initialize database
        init_db = input("\n🗄️  Initialize database now? (y/n): ").lower()
        if init_db == 'y':
            initialize_database()
        else:
            print("⚠️  Skipping database initialization.")
            print("   Run 'python run.py' to initialize it later.")
        
        # Print next steps
        print_next_steps()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()


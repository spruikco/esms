from enhanced_app import app
from extensions import db
import os

# Make sure the app context is active
with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    
    print("Creating all tables...")
    db.create_all()
    
    # Optional: Create sample user for development
    from models import User
    admin = User(
        username="admin",
        email="admin@example.com"
    )
    admin.set_password("password")
    db.session.add(admin)
    db.session.commit()
    print("Created admin user (username: admin, password: password)")
    
    print("Database initialized successfully!")
    print("\nYou can now run generate_team.py to create sample teams and players.")
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, Base, engine
from app.models.user import User

# Ensure tables are created
Base.metadata.create_all(bind=engine)

def seed_admin():
    db = SessionLocal()
    # Check if admin already exists
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("Admin user already exists!")
    else:
        admin = User(username="admin", password="password123", role="admin")
        db.add(admin)
        db.commit()
        print("Admin user 'admin' with password 'password123' created successfully.")
    
    db.close()

if __name__ == "__main__":
    seed_admin()

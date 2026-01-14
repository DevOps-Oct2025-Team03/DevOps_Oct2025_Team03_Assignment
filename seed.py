# seed.py - for testing of hashing of pw for dev epic 2
from app import create_app
from app.database import db, User, File

app = create_app()
with app.app_context():
    # Clear existing data to prevent duplicates
    db.drop_all()
    db.create_all()

    # 1. Create an Admin (Credential Protection Test)
    admin = User(username="admin_user", role="admin")
    admin.set_password("admin123") # Hashes via Bcrypt
    
    # 2. Create a Regular User
    user_a = User(username="user_a", role="user")
    user_a.set_password("user123")

    db.session.add_all([admin, user_a])
    db.session.commit()

    # 3. Create a File for User A (Data Isolation Test)
    file_a = File(original_filename="secret.txt", owner_id=user_a.id)
    db.session.add(file_a)
    db.session.commit()

    print("✅ Database seeded with Admin, User, and isolated files!")
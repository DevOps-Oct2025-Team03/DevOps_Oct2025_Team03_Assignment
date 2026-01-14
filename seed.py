# seed.py (updated section)
from app import create_app
from app.database import db, User, File

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(username="admin_user", role="admin")
    admin.set_password("admin123")
    
    user_a = User(username="user_a", role="user")
    user_a.set_password("user123")

    db.session.add_all([admin, user_a])
    db.session.commit() # Save users first so they get IDs

    # Create file with ALL required fields to pass NOT NULL constraints
    file_a = File(
        original_filename="secret.txt",
        stored_filename="abcdef12345.txt", # Added to pass constraint
        size_bytes=1024,                   # Added to pass constraint
        owner_id=user_a.id
    )
    db.session.add(file_a)
    db.session.commit()

    print("✅ Database Seeded Successfully with all constraints met!")
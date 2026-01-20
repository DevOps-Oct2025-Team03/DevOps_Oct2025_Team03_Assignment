# app/seed.py
from .database import db, User

def seed():
    # Prevent duplicate seeding
    if User.query.first():
        print("ℹ️ Database already seeded. Skipping.")
        return

    admin = User(username="admin_user", role="admin")
    admin.set_password("admin123")

    user_a = User(username="user_a", role="user")
    user_a.set_password("user123")

    db.session.add_all([admin, user_a])
    db.session.commit()

    print("✅ Database seeded automatically.")

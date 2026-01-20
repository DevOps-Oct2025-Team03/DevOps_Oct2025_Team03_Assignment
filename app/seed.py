# # app/seed.py
# from .database import db, User

# def seed():
#     # Prevent duplicate seeding
#     if User.query.first():
#         print("ℹ️ Database already seeded. Skipping.")
#         return

#     admin = User(username="admin_user", role="admin")
#     admin.set_password("admin123")

#     user_a = User(username="user_a", role="user")
#     user_a.set_password("user123")

#     db.session.add_all([admin, user_a])
#     db.session.commit()

#     print("✅ Database seeded automatically.")


from .database import db, User, File


from .database import db, User

def seed():
    # Admin user
    admin = User.query.filter_by(username="admin_user").first()
    if not admin:
        admin = User(username="admin_user", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)

    # Normal user
    user = User.query.filter_by(username="user_a").first()
    if not user:
        user = User(username="user_a", role="user")
        user.set_password("user123")
        db.session.add(user)

    db.session.commit()


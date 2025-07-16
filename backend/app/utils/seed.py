from sqlalchemy.orm import Session
from app.models import User
from app.auth import get_password_hash
import os

def seed_admin(db: Session):
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not (admin_email and admin_username and admin_password):
        print("[SEED] Skipping admin seed — missing env variables.")
        return

    existing_admin = db.query(User).filter(User.role == "admin").first()

    if existing_admin:
        print("[SEED] Admin already exists.")
        return

    admin_user = User(
        username=admin_username,
        email=admin_email,
        password=get_password_hash(admin_password),
        role="admin"
    )

    db.add(admin_user)
    db.commit()
    print("[SEED] Admin user created.")

import os
from sqlalchemy import select
from .db import AsyncSessionLocal
from app.models import User
from app.core.security import get_password_hash

async def seed_data_async():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        if result.scalars().first():
            print("⚠️ Database already seeded.")
            return

        admin = User(
            username=os.getenv("ADMIN_USERNAME", "admin"),
            email=os.getenv("ADMIN_EMAIL", "admin@example.com"),
            password=get_password_hash(os.getenv("ADMIN_PASSWORD", "admin123")),
            role="admin"
        )

        session.add(admin)
        await session.commit()
        print("✅ Admin user created.")

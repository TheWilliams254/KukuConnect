from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base, SessionLocal
from app.routes import users, products
from app.utils.seed import seed_admin
from app import models 

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    seed_admin(db)
    db.close()

    yield  # App is now running

app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/auth", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base, SessionLocal
from app.routes import users, products
from app.utils.seed import seed_admin
from app import models 

#Lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    seed_admin(db)
    db.close()

    yield

#Instantiating FastAPI with lifespan
app = FastAPI(lifespan=lifespan) 
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,         
    allow_methods=["*"],            
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/auth", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])

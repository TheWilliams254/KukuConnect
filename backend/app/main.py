from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db import engine, Base, AsyncSessionLocal
from app.api import auth, order, product
from app.seed import seed_data_async
from app.models import User, Product, Order

#Lifespan event@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await seed_data_async()
    except Exception as e:
        print(f"[Startup Error] {e}")
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

@app.get("/")
async def root():
    return {"message": "Your API is up and running"}

app.mount("/static", StaticFiles(directory="app/static"), name="static")
# app.include_router(auth.router, prefix="/auth", tags=["Users"])
app.include_router(auth.router)
app.include_router(product.router, tags=["Products"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])
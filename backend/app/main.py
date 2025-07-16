from fastapi import FastAPI
from app.routes import users, products
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/auth")
app.include_router(products.router, prefix="/products")

@app.get("/")
def read_root():
    return {"message": "Welcome to KukuConnect API 🐔"}

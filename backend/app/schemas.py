from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    # role: str
class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ProductOut(ProductCreate):
    id: int
    created_at: str

    class Config:
        orm_mode = True
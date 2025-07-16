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
    role: str
class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    image_url: Optional[str]
    created_at: Optional[str]

class ProductOut(ProductCreate):
    id: int
    created_at: str

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    status: str
    created_at: str

    class Config:
        orm_mode = True

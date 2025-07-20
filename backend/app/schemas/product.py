from pydantic import BaseModel
from typing import Optional

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
        from_attributes = True

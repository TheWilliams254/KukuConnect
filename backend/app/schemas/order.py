from pydantic import BaseModel

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
        from_attributes = True

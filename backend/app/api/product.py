from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.models import Product, User
from app.schemas.product import ProductCreate, ProductOut
from typing import List
from app.core.security import get_current_user
import shutil
import os

router = APIRouter()
UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create product (admin only)
@router.post("/products", response_model=ProductOut)
async def create_product(
    name: str = Form(...),
    price: float = Form(...),
    description: str = Form(None),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can add products")

    image_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    image_url = f"/static/uploads/{image.filename}"

    new_product = Product(
        name=name,
        price=price,
        description=description,
        image_url=image_url
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


# Get all products
@router.get("/products", response_model=List[ProductOut])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products


# Delete product (admin only)
@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete products")

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()
    return {"message": "Product deleted successfully"}


# Update product (admin only)
@router.put("/products/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update products")

    result = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_data.dict().items():
        setattr(db_product, key, value)

    await db.commit()
    await db.refresh(db_product)
    return db_product

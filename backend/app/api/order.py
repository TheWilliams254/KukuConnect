from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_db
from app.models import Order, Product, User
from app.schemas.order import OrderCreate, OrderOut
from app.api.auth import get_current_user
from datetime import datetime
from typing import List

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = await db.execute(select(Product).where(Product.id == order_data.product_id))
    product = query.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if order_data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    new_order = Order(
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        user_id=current_user.id,
        status="pending",
        created_at=datetime.utcnow()
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

@router.get("/my-orders", response_model=List[OrderOut])
async def get_my_orders(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Order).where(Order.user_id == current_user.id))
    return result.scalars().all()


@router.get("/", response_model=List[OrderOut])
async def get_all_orders(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only.")
    result = await db.execute(select(Order))
    return result.scalars().all()


@router.patch("/{order_id}")
async def update_order_status(order_id: int, status: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only.")

    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    await db.commit()
    return {"message": "Order status updated"}

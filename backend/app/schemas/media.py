from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class MediaCreate(BaseModel):
    report_id: Optional[UUID] = None


class MediaOut(BaseModel):
    id: UUID
    file_url: str = Field(..., example="/uploads/abc123.jpg")
    file_type: str = Field(..., example="image/jpeg")
    report_id: Optional[UUID]
    user_id: UUID

    class Config:
        orm_mode = True
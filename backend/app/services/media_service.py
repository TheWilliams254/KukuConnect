import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
import aiofiles
import os

from app.models.media import Media
from uuid import UUID


UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)



async def save_media(
    file: UploadFile,
    user_id: UUID,
    db: AsyncSession,
    report_id: Optional[UUID] = None
) -> Media:
    if file.content_type not in ["image/jpeg", "image/png", "video/mp4"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = UPLOAD_DIR / filename

    async with aiofiles.open(filepath, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    file_url = f"/static/uploads/{filename}"

    media = Media(
        file_url=file_url,
        file_type=file.content_type,
        user_id=user_id,
        report_id=report_id
    )

    db.add(media)
    await db.commit()
    await db.refresh(media)
    return media



async def delete_media(
    media_id: UUID,
    user_id: UUID,
    db: AsyncSession,
    is_admin: bool = False
):
    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalar_one_or_none()

    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    if media.user_id != user_id and not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this media")

    
    file_path = UPLOAD_DIR / Path(media.file_url).name
    if file_path.exists():
        os.remove(file_path)

    
    await db.delete(media)
    await db.commit()

    return {"message": "Media deleted successfully"}
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey
from uuid import UUID, uuid4
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from app.db import Base

class Media(Base):
    __tablename__ = "media"

    id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid4)
    file_url: Mapped[str] = mapped_column(String, nullable=False)
    file_type: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    report_id: Mapped[Optional[UUID]] = mapped_column(pgUUID(as_uuid=True), ForeignKey("reports.id", ondelete="CASCADE"), nullable=True)

    user = relationship("User", back_populates="media")
    report = relationship("Report", back_populates="media")
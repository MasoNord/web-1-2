from src.harmony_hound.domain.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, func, DateTime, text
from datetime import datetime

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    lang: Mapped[str] = mapped_column(String(10), nullable=False)
    api_calls: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"
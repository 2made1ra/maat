from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import String, Integer, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class CategoryEnum(str, Enum):
    MOVIE = "movie"
    SERIES = "series"
    ANIME = "anime"
    BOOK = "book"
    GAME = "game"
    MUSIC = "music"
    OTHER = "other"

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[CategoryEnum] = mapped_column(String(50), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 to 10
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<Review(id={self.id}, title='{self.title}', category='{self.category}', score={self.score})>"

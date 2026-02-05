from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from database import db



class Word(db.Model):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Boolean, Enum as SAEnum, DateTime
from database import db
from enum import Enum
from datetime import datetime

class Word(db.Model):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    games:Mapped[list["Game"]] = relationship(back_populates='word', uselist=True)


class StatusType(Enum):
    ACTIVE= "ACTIVE"
    WON= "WON"
    LOST="LOST"


class Game(db.Model):
    __tablename__="games"

    id:Mapped[int] = mapped_column(Integer, primary_key= True)
    player:Mapped[str] = mapped_column(String(25), nullable=False)
    status:Mapped[StatusType] = mapped_column(SAEnum(StatusType), default=StatusType.ACTIVE, nullable=False)
    attempt:Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_attempt:Mapped[int] = mapped_column(Integer, default=6, nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    finished_at:Mapped[datetime] = mapped_column(DateTime)
    word_id:Mapped[int]= mapped_column(Integer, ForeignKey("words.id"), nullable=False)
    
    word:Mapped["Word"]= relationship(back_populates='games')
    guesses:Mapped[list["Guess"]]= relationship(back_populates='game', uselist=True)


class Guess(db.Model):
    __tablename__="guesses"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    attempt_no:Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    guess:Mapped[str] = mapped_column(String(10), nullable=False)
    result:Mapped[str] = mapped_column(String(10), nullable=False)
    game_id:Mapped[int] = mapped_column(Integer, ForeignKey("games.id"), nullable=False)

    game:Mapped["Game"]= relationship(back_populates='guesses')
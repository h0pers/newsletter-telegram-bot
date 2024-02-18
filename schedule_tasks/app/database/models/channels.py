import datetime

from sqlalchemy import BigInteger, String, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.main import Base


class Channels(Base):
    __tablename__ = 'channels'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id = mapped_column(BigInteger(), unique=True)
    chat_username = mapped_column(String(32))
    creation_date: Mapped[datetime.datetime] = mapped_column(Date(), server_default=func.current_date())
    static_tasks = relationship('BotMessageTasks', back_populates="reply_chat", cascade="all, delete")
    periodic_tasks = relationship('BotPeriodicMessageTasks', back_populates="reply_chat", cascade="all, delete")

import datetime

from sqlalchemy import BigInteger, ForeignKey, Integer, Time, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .channels import Channels

from app.database.main import Base


class MessageCategory(Base):
    __tablename__ = 'bot_message_categories'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(40), unique=True)
    tasks = relationship('BotMessageTasks', back_populates='category', cascade='all, delete')


class BotMessageTasks(Base):
    __tablename__ = 'bot_message_tasks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(Integer())
    message_thread_id: Mapped[int] = mapped_column(Integer(), nullable=True)
    publish_time: Mapped[datetime.time] = mapped_column(Time())
    from_chat_id = mapped_column(BigInteger())
    reply_chat_id = mapped_column(ForeignKey("channels.id"))
    reply_chat = relationship('Channels', back_populates="tasks", cascade="save-update")
    category_id = mapped_column(ForeignKey('bot_message_categories.id'))
    category = relationship('MessageCategory', back_populates='tasks', cascade="save-update")
    was_published_last_time: Mapped[bool] = mapped_column(Boolean(), default=False)

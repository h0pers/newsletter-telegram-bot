import datetime

from sqlalchemy import BigInteger, ForeignKey, Integer, Time, Interval, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .channels import Channels

from app.database.main import Base


class BotMessageTasks(Base):
    __tablename__ = 'bot_message_tasks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(Integer())
    message_thread_id: Mapped[int] = mapped_column(Integer(), nullable=True)
    publish_time: Mapped[datetime.time] = mapped_column(Time())
    from_chat_id = mapped_column(BigInteger())
    reply_chat_id = mapped_column(ForeignKey("channels.id"))
    reply_chat = relationship('Channels', back_populates="static_tasks", cascade="save-update")


class BotPeriodicMessageTasks(Base):
    __tablename__ = 'bot_periodic_message_tasks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(Integer())
    message_thread_id: Mapped[int] = mapped_column(Integer(), nullable=True)
    last_publish_time: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=func.now(),
                                                                 server_onupdate=func.now())
    time_interval: Mapped[datetime.timedelta] = mapped_column(Interval())
    from_chat_id = mapped_column(BigInteger())
    reply_chat_id = mapped_column(ForeignKey("channels.id"))
    reply_chat = relationship('Channels', back_populates="periodic_tasks", cascade="save-update")

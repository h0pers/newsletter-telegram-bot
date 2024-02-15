from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

from bot.config import DB_URL, SCHEDULE_DB_URL

engine = create_async_engine(DB_URL, echo=True)

tasks_db_engine = create_async_engine(SCHEDULE_DB_URL, echo=True)

tasks_db_session_local = async_sessionmaker(autocommit=False, autoflush=False, bind=tasks_db_engine)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

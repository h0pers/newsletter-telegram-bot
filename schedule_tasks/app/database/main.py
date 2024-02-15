from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

from app.config import DB_URL

engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

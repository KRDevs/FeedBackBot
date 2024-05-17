from sqlalchemy import ForeignKey, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from datetime import datetime
from typing import List

engine = create_async_engine(
    'sqlite+aiosqlite:///db.sqlite3',
    echo=True,
)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    number: Mapped[str] = mapped_column(String(20), nullable=True)
    username: Mapped[str] = mapped_column(String(30), nullable=True)


class Requirement(Base):
    __tablename__ = 'requirements'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(2048))
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

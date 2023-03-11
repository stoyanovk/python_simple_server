from typing import List
from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
    LargeBinary,
)
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from db.pg_context import engine


class Base(DeclarativeBase):
    pass


class People(Base):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    last_visit: Mapped[DateTime | None] = mapped_column(DateTime)
    view_count: Mapped[int]
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="people")


# back_populates= ??


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    password: Mapped[LargeBinary] = mapped_column(LargeBinary())
    people: Mapped[List["People"]] = relationship(back_populates="user")


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

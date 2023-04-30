from sqlalchemy import (
    String,
    LargeBinary,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.init_db import reg


@reg.mapped_as_dataclass()
class Users:
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    password: Mapped[bytes] = mapped_column(LargeBinary())
    people: Mapped[list["People"]] = relationship(back_populates="user")

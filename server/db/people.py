from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.init_db import reg


@reg.mapped_as_dataclass()
class People:
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    last_visit: Mapped[DateTime | None] = mapped_column(DateTime)
    view_count: Mapped[int]
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="people")

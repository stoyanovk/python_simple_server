from sqlalchemy import (
    String,
    ForeignKey,
)

from sqlalchemy.orm import mapped_column, Mapped
from db.init_db import reg


@reg.mapped_as_dataclass()
class Prayers:
    __tablename__ = "prayers"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    text: Mapped[str] = mapped_column(String(10000))
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

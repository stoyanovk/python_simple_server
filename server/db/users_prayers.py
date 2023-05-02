from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from db.init_db import reg


@reg.mapped_as_dataclass()
class Users_prayers:
    __tablename__ = "users_prayers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    prayer_id: Mapped[int] = mapped_column(ForeignKey("prayers.id"))

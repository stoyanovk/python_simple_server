from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from db.init_db import reg


@reg.mapped_as_dataclass()
class Users_prayers:
    __tablename__ = "users_prayers"
    id: Mapped[int] = mapped_column(primary_key=True)
    # Я не уверен в этом ondelete="CASCADE" для user_id, если я правильно
    # понимаю как он работает то при удалении prayer должен быть удален юзер
    #  но у меня не работает скрипт python fill_db.py если его нет
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    prayer_id: Mapped[int] = mapped_column(ForeignKey("prayers.id", ondelete="CASCADE"))

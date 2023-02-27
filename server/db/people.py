from sqlalchemy import Integer, String, Column, ForeignKey
from db.init_db import Base


# meta = MetaData()


# user_names = Table(
#     "user_names",
#     meta,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("user_names", String(200), nullable=False),
# )
class People(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))

from db.session import session, Base
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column
class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(256), nullable=False)
    first_name: Mapped[str] = mapped_column(String(256), nullable=False)
    last_name: Mapped[str] = mapped_column(String(256), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

class InfoBot(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('users.chat_id'))
    token: Mapped[str] = mapped_column(String(256), nullable=False)
    botlink: Mapped[str] = mapped_column(String(256), nullable=False)
    payedtill : Mapped[DateTime] = mapped_column(DateTime, nullable=False)


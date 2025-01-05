from db.session import Base
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Column, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
class User(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(256), nullable=False)
    first_name: Mapped[str] = mapped_column(String(256), nullable=False)
    promocode: Mapped[str] = mapped_column(String(256), nullable=True)
    marketer: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False,)

class InfoBot(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.chat_id'))
    token: Mapped[str] = mapped_column(String(256), nullable=False)
    botlink: Mapped[str] = mapped_column(String(256), nullable=False)
    payedtill : Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    company_name: Mapped[str] = mapped_column(String(256), nullable=True)

class Promo(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    promocode: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    referal: Mapped[str] = mapped_column(String(256), nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.chat_id'), nullable=False)
    expire_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
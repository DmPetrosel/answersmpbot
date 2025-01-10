from db.session import Base
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Column, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
import sqlalchemy as sa
class User(Base):
    id_seq = sa.Sequence("seq_user_id", metadata=Base.metadata)

    # id: Mapped[int] = mapped_column(BigInteger, unique=False, autoincrement=True, default=id_seq.next_value(), server_default=id_seq.next_value())
    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(256), nullable=False)
    first_name: Mapped[str] = mapped_column(String(256), nullable=False)
    promocode: Mapped[str] = mapped_column(String(256), nullable=True)
    marketer: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    balance: Mapped[int] = mapped_column(BigInteger, nullable=True, default=0, server_default='0')

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
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    referal: Mapped[str] = mapped_column(String(256), nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.chat_id'), nullable=False)
    expire_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    user = relationship("User", backref="promocodes")
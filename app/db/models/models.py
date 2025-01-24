from db.session import Base
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Column, BigInteger
from sqlalchemy.orm import relationship, backref
import sqlalchemy as sa
class User(Base):
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(256), nullable=False)
    first_name = Column(String(256), nullable=False)
    promocode = Column(String(256), nullable=True)
    marketer = Column(Boolean, default=False, server_default="false", nullable=False)
    balance = Column(BigInteger, nullable=True, default=0, server_default='0')
    # promos = relationship("Promo", back_populates="user", lazy='joined', cascade='all, delete-orphan', uselist=True)

class InfoBot(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey('users.chat_id'))
    token = Column(String(256), nullable=False)
    botlink = Column(String(256), nullable=False)
    payedtill = Column(String(256), nullable=False)
    company_name = Column(String(256), nullable=True)
    user = relationship("User", backref='infobots', lazy='joined', uselist=False)

class Promo(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    promocode = Column(String(256), nullable=False, unique=True)
    price = Column(BigInteger, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    referal = Column(String(256), nullable=False)
    chat_id = Column(BigInteger, ForeignKey('users.chat_id'), nullable=False)
    expire_date = Column(String(20), nullable=True)
    user = relationship("User", backref="promos", lazy='joined', uselist=False)
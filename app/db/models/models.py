from db.session import Base
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Column, BigInteger, ARRAY, Date
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

class Register(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    chat_id = Column(BigInteger, nullable=False)
    username = Column(String(256), nullable=False)
    name = Column(String(256), nullable=False)
    bot_username = Column(String(256), ForeignKey('infobots.bot_username', ondelete='cascade'), nullable=False)
    approve = Column(Boolean, nullable=False, default=False)

class InfoBot(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey('users.chat_id'), nullable=False)
    token = Column(String(256), nullable=False)
    bot_username = Column(String(256), nullable=True, unique=True)
    # payedtill = Column(Date, nullable=False)
    company_name = Column(String(256), nullable=True)
    samples_ans = Column(ARRAY(String(400)), nullable=True)
    wb_token = Column(String(256), nullable=True)
    user = relationship("User", backref='infobots', lazy='joined', uselist=False)

class Promo(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    promocode = Column(String(256), nullable=False, unique=True)
    price = Column(BigInteger, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    referal = Column(String(256), nullable=False)
    chat_id = Column(BigInteger, ForeignKey('users.chat_id'), nullable=False)
    expire_date = Column(Date, nullable=True)
    user = relationship("User", backref="promos", lazy='joined', uselist=False)

class WBFeedData(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    mess_ids = Column(ARRAY(BigInteger), nullable=True)
    feed_id = Column(BigInteger, nullable=False)
    feed_mess = Column(String(1024), nullable=True)
    feed_ans = Column(String(1024), nullable=True)
from db.session import Base
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Column, BigInteger, ARRAY, Date, Float, Double
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import sqlalchemy as sa
class User(Base):
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(256), nullable=False)
    first_name = Column(String(256), nullable=False)
    promocode = Column(String(256), nullable=True)
    marketer = Column(Boolean, default=False, server_default="false", nullable=False)
    balance = Column(Float, nullable=False, default=0, server_default='0')
    registration_day = Column(Date, nullable=False, default=datetime.today().date, server_default=f"{datetime.today().strftime('%Y-%m-%d')}")
    is_payed_first_time = Column(Boolean, nullable=False, default=False, server_default='false')
    payout = Column(Float, nullable=False, default=0, server_default='0')
    # promos = relationship("Promo", back_populates="user", lazy='joined', cascade='all, delete-orphan', uselist=True)

class Register(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    chat_id = Column(BigInteger, nullable=False)
    username = Column(String(256), nullable=False)
    name = Column(String(256), nullable=False)
    principal_chat_id = Column(BigInteger, ForeignKey('users.chat_id', ondelete='cascade'), nullable=True)
    bot_username = Column(String(256), ForeignKey('infobots.bot_username', ondelete='cascade'), nullable=False)
    approve = Column(Boolean, nullable=False, default=False)
    automated_type = Column(String(256), nullable=True, default="half-auto", server_default='half-auto')
    user = relationship("User", backref='registers', lazy="joined", uselist=False)

class InfoBot(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey('users.chat_id', ondelete='cascade'), nullable=False)
    token = Column(String(256), nullable=False)
    bot_username = Column(String(256), nullable=True, unique=True)
    # payedtill = Column(Date, nullable=False)
    company_name = Column(String(256), nullable=True)
    samples_ans = Column(ARRAY(String(400)), nullable=True)
    number_of_art = Column(Integer, nullable=True)
    wb_token = Column(String(1024), nullable=True)
    company_description = Column(String(1024), nullable=True) 
    user = relationship("User", backref='infobots', lazy='joined', uselist=False)

class Promo(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    promocode = Column(String(256), nullable=False, unique=True)
    price = Column(BigInteger, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    referal = Column(String(256), nullable=False)
    chat_id = Column(BigInteger, ForeignKey('users.chat_id', ondelete='cascade'), nullable=False)
    expire_date = Column(Date, nullable=True)
    user = relationship("User", backref="promos", lazy='joined', uselist=False)

class WBFeedData(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    mess_ids = Column(ARRAY(BigInteger), nullable=True)
    product_name = Column(String(256), nullable=True)
    product_nmId = Column(BigInteger)
    feed_id = Column(String(256), nullable=False)
    feed_mess = Column(String(1024), nullable=True)
    feed_ans = Column(String(1024), nullable=True)
    createdDate = Column(DateTime, nullable=False)
    time_now = Column(DateTime, nullable=False)
    bot_username = Column(String(256), nullable=False)
    valuation = Column(Float, nullable=True)
    materials_links = Column(String(1024), nullable=True)
    is_new = Column(Boolean, nullable=False, default=True)
    is_answering = Column(Boolean, nullable=False, default=False)
    answering_chat_id = Column(BigInteger, nullable=True)
    customer_name = Column(String(256), nullable=True)
    ai_usage = Column(String(256), nullable=True, default="ai", server_default="ai")

class WBFeedAnswer(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    mess_id = Column(BigInteger, nullable=True, autoincrement=True)
    chat_id = Column(BigInteger)
    question_id = Column(BigInteger, ForeignKey('wbfeeddatas.id', ondelete='cascade'), nullable=False)
    text = Column(String(1024), nullable=False)
    total_tokens = Column(BigInteger, nullable=True)

class MoneyStat(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    chat_id = Column(BigInteger, nullable=False)
    invoice_id = Column(String(256), nullable=True)
    amount = Column(BigInteger, nullable=False)
    invoice_payload = Column(String(256), nullable=False, default="income", server_default='income')
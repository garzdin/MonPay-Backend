from sqlalchemy import create_engine, event, Column, Integer, Float, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from settings import DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME
from utils.db import construct_url

__all__ = ['User', 'Account', 'Transaction', 'session']

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    ref = Column(String, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    entity_type = Column(Integer)
    street = Column(String)
    city = Column(String)
    state_or_province = Column(String)
    postal_code = Column(Integer)
    country = Column(Integer)
    bank_country = Column(String)
    id_type = Column(Integer)
    id_value = Column(String)
    is_admin = Column(Boolean, default=False)
    accounts = relationship("Account")
    beneficiaries = relationship("Beneficiary")
    transactions = relationship("Transaction")
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)

@event.listens_for(User, 'before_insert')
def user_before_insert(mapper, connection, target):
    target.created_on = datetime.now()
    target.version = 1

@event.listens_for(User, 'before_update')
def user_before_update(mapper, connection, target):
    target.updated_on = datetime.now()
    target.version += 1


class Beneficiary(Base):
    __tablename__ = 'beneficiaries'

    id = Column(Integer, primary_key=True)
    ref = Column(String, unique=True)
    name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    country = Column(String)
    email = Column(String)
    address = Column(String)
    city = Column(String)
    state_or_province = Column(String)
    postal_code = Column(Integer)
    country = Column(Integer)
    default = Column(Boolean, default=False)
    type = Column(Integer)
    company = Column(String)
    id_type = Column(Integer)
    id_value = Column(String)
    type = Column(Integer)
    user = Column(Integer, ForeignKey('users.id'))
    accounts = relationship("Account")
    transactions = relationship("Transaction")
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)

@event.listens_for(Beneficiary, 'before_insert')
def user_before_insert(mapper, connection, target):
    target.created_on = datetime.now()
    target.version = 1

@event.listens_for(Beneficiary, 'before_update')
def user_before_update(mapper, connection, target):
    target.updated_on = datetime.now()
    target.version += 1


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    iban = Column(String, nullable=False)
    bic_swift = Column(String, nullable=False)
    currency = Column(Integer)
    country = Column(Integer)
    type = Column(Integer)
    user = Column(Integer, ForeignKey('users.id'))
    beneficiary = Column(Integer, ForeignKey('beneficiaries.id'))
    transactions = relationship("Transaction")
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)

@event.listens_for(Account, 'before_insert')
def user_before_insert(mapper, connection, target):
    target.created_on = datetime.now()
    target.version = 1

@event.listens_for(Account, 'before_update')
def user_before_update(mapper, connection, target):
    target.updated_on = datetime.now()
    target.version += 1


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    ref = Column(String, unique=True)
    amount = Column(Float)
    currency = Column(Integer)
    reason = Column(String)
    reference = Column(String)
    type = Column(Integer)
    completed = Column(Boolean, default=False)
    user = Column(Integer, ForeignKey('users.id'))
    beneficiary = Column(Integer, ForeignKey('beneficiaries.id'))
    account = Column(Integer, ForeignKey('accounts.id'))
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)

@event.listens_for(Transaction, 'before_insert')
def user_before_insert(mapper, connection, target):
    target.created_on = datetime.now()
    target.version = 1

@event.listens_for(Transaction, 'before_update')
def user_before_update(mapper, connection, target):
    target.updated_on = datetime.now()
    target.version += 1

engine = create_engine(construct_url('postgres', DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME))
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

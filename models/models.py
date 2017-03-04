from sqlalchemy import create_engine, event, Column, Integer, Float, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from settings import DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME
from utils.db import construct_url

__all__ = ['User', 'Account', 'Transaction', 'session']

Base = declarative_base()


class Id(object):
    id = Column(Integer, primary_key=True)


class Entity(object):
    entity_type = {
        0: "private",
        1: "company"
    }

    entity_type = Column(Integer, default=0)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class Birth(object):
    date_of_birth = Column(Date)


class Phone(object):
    phone_number = Column(String)


class Identity(object):
    id_type = {
        0: "id",
        1: "passport"
    }

    id_type = Column(Integer)
    id_value = Column(String)


class Version(object):
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)


class User(Base, Id, Entity, Birth, Phone, Identity, Version):
    __tablename__ = 'users'

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    address = relationship("Address", uselist=False)
    is_admin = Column(Boolean, default=False)
    accounts = relationship("Account")
    beneficiaries = relationship("Beneficiary")
    transactions = relationship("Transaction")

@event.listens_for(User, 'before_insert')
def user_before_insert(mapper, connection, target):
    target.created_on = datetime.now()
    target.version = 1

@event.listens_for(User, 'before_update')
def user_before_update(mapper, connection, target):
    target.updated_on = datetime.now()
    target.version += 1


class Beneficiary(Base, Id, Entity, Phone, Identity, Version):
    __tablename__ = 'beneficiaries'

    email = Column(String)
    user = Column(Integer, ForeignKey('users.id'))
    account = relationship("Account", uselist=False)
    transactions = relationship("Transaction")

@event.listens_for(Beneficiary, 'before_insert')
def beneficiary_before_insert(mapper, connection, target):
    target.created_on = datetime.now()
    target.version = 1

@event.listens_for(Beneficiary, 'before_update')
def beneficiary_before_update(mapper, connection, target):
    target.updated_on = datetime.now()
    target.version += 1


class Account(Base, Id, Version):
    __tablename__ = 'accounts'

    iban = Column(String, nullable=False)
    bic_swift = Column(String)
    currency = relationship("Currency", uselist=False)
    country = Column(String)
    active = Column(Boolean, default=False)
    user = Column(Integer, ForeignKey('users.id'))
    beneficiary = Column(Integer, ForeignKey('beneficiaries.id'))
    transactions = relationship("Transaction")

@event.listens_for(Account, 'before_insert')
def account_before_insert(mapper, connection, target):
    target.created_on = datetime.now()
    target.version = 1

@event.listens_for(Account, 'before_update')
def account_before_update(mapper, connection, target):
    target.updated_on = datetime.now()
    target.version += 1


class Currency(Base, Id, Version):
    __tablename__ = 'currencies'

    iso_code = Column(String(3), nullable=False)
    dispay_name = Column(String)
    account = Column(Integer, ForeignKey('accounts.id'))
    transaction = Column(Integer, ForeignKey('transactions.id'))


class Transaction(Base, Id, Version):
    __tablename__ = 'transactions'

    reference = Column(String)
    amount = Column(Float)
    currency = relationship("Currency", uselist=False)
    reason = Column(String)
    completed = Column(Boolean, default=False)
    user = Column(Integer, ForeignKey('users.id'))
    beneficiary = Column(Integer, ForeignKey('beneficiaries.id'))
    account = Column(Integer, ForeignKey('accounts.id'))

@event.listens_for(Transaction, 'before_insert')
def transaction_before_insert(mapper, connection, target):
    target.created_on = datetime.now()
    target.version = 1

@event.listens_for(Transaction, 'before_update')
def transaction_before_update(mapper, connection, target):
    target.updated_on = datetime.now()
    target.version += 1


class Address(Base, Id, Version):
    __tablename__ = 'addresses'

    address = Column(String)
    city = Column(String)
    state_or_province = Column(String)
    postal_code = Column(Integer)
    country = Column(String)
    user = Column(Integer, ForeignKey('users.id'))

@event.listens_for(Address, 'before_insert')
def address_before_insert(mapper, connection, target):
    target.created_on = datetime.now()
    target.version = 1

@event.listens_for(Address, 'before_update')
def address_before_update(mapper, connection, target):
    target.updated_on = datetime.now()
    target.version += 1

engine = create_engine(construct_url('postgres', DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME))
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

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


class Version(object):
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)


class Identity(object):
    id_type = {
        0: "id",
        1: "passport"
    }

    id_type = Column(Integer)
    id_value = Column(String)


class Entity(object):
    entity_type = {
        0: "private",
        1: "company"
    }

    entity_type = Column(Integer)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date)


class Phone(object):
    phone_number = Column(String)


class User(Base, Id, Entity, Identity, Version, Phone):
    __tablename__ = 'users'

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    address = relationship("Address", uselist=False, back_populates="user")
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


class Beneficiary(Base, Id, Entity, Identity, Version, Phone):
    __tablename__ = 'beneficiaries'

    email = Column(String)
    address = relationship("Address", uselist=False, back_populates="beneficiary")
    user = Column(Integer, ForeignKey('users.id'))
    accounts = relationship("Account")
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
    bic_swift = Column(String, nullable=False)
    currency = Column(String)
    country = Column(String)
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


class Transaction(Base, Id, Version):
    __tablename__ = 'transactions'

    reference = Column(String)
    amount = Column(Float)
    currency = Column(String)
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
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="address")
    beneficiary_id = Column(Integer, ForeignKey('beneficiaries.id'))
    beneficiary = relationship("Beneficiary", back_populates="address")

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

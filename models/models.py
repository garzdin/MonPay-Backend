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
    entity_type = Column(Integer)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = relationship("Address", uselist=False, back_populates="users")
    date_of_birth = Column(Date)
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
    entity_type = Column(Integer)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    address = relationship("Address", uselist=False, back_populates="users")
    date_of_birth = Column(Date)
    id_type = Column(Integer)
    id_value = Column(String)
    user = Column(Integer, ForeignKey('users.id'))
    accounts = relationship("Account")
    transactions = relationship("Transaction")
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)

@event.listens_for(Beneficiary, 'before_insert')
def beneficiary_before_insert(mapper, connection, target):
    target.created_on = datetime.now()
    target.version = 1

@event.listens_for(Beneficiary, 'before_update')
def beneficiary_before_update(mapper, connection, target):
    target.updated_on = datetime.now()
    target.version += 1


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    iban = Column(String, nullable=False)
    bic_swift = Column(String, nullable=False)
    currency = Column(String)
    country = Column(String)
    user = Column(Integer, ForeignKey('users.id'))
    beneficiary = Column(Integer, ForeignKey('beneficiaries.id'))
    transactions = relationship("Transaction")
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)

@event.listens_for(Account, 'before_insert')
def account_before_insert(mapper, connection, target):
    target.created_on = datetime.now()
    target.version = 1

@event.listens_for(Account, 'before_update')
def account_before_update(mapper, connection, target):
    target.updated_on = datetime.now()
    target.version += 1


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    reference = Column(String)
    amount = Column(Float)
    currency = Column(String)
    reason = Column(String)
    completed = Column(Boolean, default=False)
    user = Column(Integer, ForeignKey('users.id'))
    beneficiary = Column(Integer, ForeignKey('beneficiaries.id'))
    account = Column(Integer, ForeignKey('accounts.id'))
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)

@event.listens_for(Transaction, 'before_insert')
def transaction_before_insert(mapper, connection, target):
    target.created_on = datetime.now()
    target.version = 1

@event.listens_for(Transaction, 'before_update')
def transaction_before_update(mapper, connection, target):
    target.updated_on = datetime.now()
    target.version += 1


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    address = Column(String)
    city = Column(String)
    state_or_province = Column(String)
    postal_code = Column(Integer)
    country = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")
    beneficiary_id = Column(Integer, ForeignKey('beneficiaries.id'))
    beneficiary = relationship("Beneficiary", back_populates="addresses")
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)

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

from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

__all__ = ['User', 'Account', 'Transaction']

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    accounts = relationship("Account")
    transactions = relationship("Transaction")
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)

    def before_insert(self):
        self.created_on = datetime.now()
        self.version = 1

    def before_update(self):
        self.updated_on = datetime.now()
        self.version += 1


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    country = Column(String, nullable=False)
    last_four = Column(String, nullable=False)
    verified = Column(Boolean, default=False)
    user = Column(Integer, ForeignKey('users.id'))
    transactions = relationship("Transaction")
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)

    def before_insert(self):
        self.created_on = datetime.now()
        self.version = 1

    def before_update(self):
        self.updated_on = datetime.now()
        self.version += 1


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    completed = Column(Boolean, default=False)
    user = Column(Integer, ForeignKey('users.id'))
    account = Column(Integer, ForeignKey('accounts.id'))
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    version = Column(Integer)

    def before_insert(self):
        self.created_on = datetime.now()
        self.version = 1

    def before_update(self):
        self.updated_on = datetime.now()
        self.version += 1

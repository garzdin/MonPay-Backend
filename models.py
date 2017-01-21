from pony.orm import *
from datetime import date, datetime
from decimal import Decimal

__all__ = ['db', 'User', 'Account', 'Transaction']

db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    stripe_id = Optional(str, unique=True)
    first_name = Optional(str)
    last_name = Optional(str)
    email = Required(str, unique=True)
    password = Required(str)
    is_admin = Required(bool, default=False)
    accounts = Set('Account')
    transactions = Set('Transaction')
    created_on = Optional(datetime)
    updated_on = Optional(datetime)
    version = Optional(int)

    def before_insert(self):
        self.created_on = datetime.now()
        self.version = 1

    def before_update(self):
        self.updated_on = datetime.now()
        self.version += 1


class Account(db.Entity):
    id = PrimaryKey(int, auto=True)
    stripe_id = Optional(str, unique=True)
    country = Required(str)
    last_four = Required(str)
    verified = Required(bool, default=False)
    user = Required(User)
    transactions = Set('Transaction')
    created_on = Optional(datetime)
    updated_on = Optional(datetime)
    version = Optional(int)

    def before_insert(self):
        self.created_on = datetime.now()
        self.version = 1

    def before_update(self):
        self.updated_on = datetime.now()
        self.version += 1


class Transaction(db.Entity):
    id = PrimaryKey(int, auto=True)
    stripe_id = Optional(str, unique=True)
    amount = Required(Decimal)
    completed = Required(bool, default=False)
    user = Required(User)
    account = Required(Account)
    created_on = Optional(datetime)
    updated_on = Optional(datetime)
    version = Optional(int)

    def before_insert(self):
        self.created_on = datetime.now()
        self.version = 1

    def before_update(self):
        self.updated_on = datetime.now()
        self.version += 1

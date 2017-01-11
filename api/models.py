from pony.orm import *
from datetime import date, datetime
from decimal import Decimal

__all__ = ['db', 'User', 'Card', 'Transaction']

db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    first_name = Optional(str)
    last_name = Optional(str)
    email = Required(str, unique=True)
    password = Required(str)
    is_admin = Required(bool, default=False)
    cards = Set('Card')
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


class Card(db.Entity):
    id = PrimaryKey(int, auto=True)
    hash = Required(str, unique=True)
    last_four = Required(str)
    expiration_date = Required(date)
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
    amount = Required(Decimal)
    completed = Required(bool, default=False)
    user = Required(User)
    card = Required(Card)
    created_on = Optional(datetime)
    updated_on = Optional(datetime)
    version = Optional(int)

    def before_insert(self):
        self.created_on = datetime.now()
        self.version = 1

    def before_update(self):
        self.updated_on = datetime.now()
        self.version += 1

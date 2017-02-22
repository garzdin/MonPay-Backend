from json import load, dumps
from falcon import HTTPBadRequest, HTTPNotFound, before
from middleware.token import validate_token
from encoders.datetime import DateTimeEncoder
from models.models import Account, session
from models.schema import AccountSchema

__all__ = ['AccountListResource', 'AccountGetResource',
           'AccountCreateResource', 'AccountUpdateResource',
           'AccountUpdateStatusResource', 'AccountDeleteResource']


class AccountListResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        """Handles GET requests"""
        accounts = session.query(Account).filter(Account.user == req.uid)
        schema = AccountSchema(many=True)
        resp.body = dumps({"accounts": schema.dump(accounts).data}, cls=DateTimeEncoder)


class AccountGetResource(object):
    @before(validate_token)
    def on_get(self, req, resp, id):
        """Handles GET requests"""
        account = session.query(Account).filter(Account.user == req.uid, Account.id == id).first()
        if not account:
            raise HTTPNotFound(description="Account not found")
        schema = AccountSchema()
        resp.body = dumps({"account": schema.dump(account).data}, cls=DateTimeEncoder)


class AccountCreateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        schema = AccountSchema()
        result = schema.load(data)
        if result.errors:
            raise HTTPBadRequest(description=result.errors)
        account = Account(**result.data)
        account.user = req.uid
        session.add(account)
        session.commit()
        result = schema.dump(account)
        resp.body = dumps({"account": result.data}, cls=DateTimeEncoder)


class AccountUpdateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        account = session.query(Account).filter(Account.user == req.uid, Account.id == data['id'])
        if not account:
            raise HTTPNotFound(description="Account not found")
        schema = AccountSchema()
        result = schema.load(data)
        if result.errors:
            raise HTTPBadRequest(description=result.errors)
        account.update(result.data)
        session.commit()
        result = schema.dump(account.first())
        resp.body = dumps({"account": result.data}, cls=DateTimeEncoder)


class AccountUpdateStatusResource(object):
    @before(validate_token)
    def on_get(self, req, resp, id):
        account = session.query(Account).filter(Account.user == req.uid, Account.id == id).first()
        if not account:
            raise HTTPNotFound(description="Account not found")
        session.query(Account).filter(Account.user == req.uid).update({"active": False})
        account.active = True
        session.commit()
        session.refresh(account)
        schema = AccountSchema()
        result = schema.dump(account)
        resp.body = dumps({"account": result.data}, cls=DateTimeEncoder)

class AccountDeleteResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'id' not in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        account = session.query(Account).filter(Account.user == req.uid, Account.id == data['id']).first()
        if not account:
            raise HTTPNotFound(description="Account not found")
        schema = AccountSchema()
        session.delete(account)
        session.commit()
        result = schema.dump(account)
        resp.body = dumps({"account": result.data}, cls=DateTimeEncoder)

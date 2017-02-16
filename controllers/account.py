from json import load, dumps
from falcon import HTTPBadRequest, HTTPNotFound, before
from middleware.token import validate_token
from models.models import Account, session

__all__ = ['AccountListResource', 'AccountGetResource',
           'AccountCreateResource', 'AccountUpdateResource',
           'AccountDeleteResource']


class AccountListResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        """Handles GET requests"""
        accounts = session.query(Account).filter(Account.user == req.uid)
        output = [{
            "id": account.id,
            "iban": account.iban,
            "bic_swift": account.bic_swift,
            "currency": account.currency,
            "country": account.country
        } for account in accounts]
        resp.body = dumps({"status": True, "accounts": output})


class AccountGetResource(object):
    @before(validate_token)
    def on_get(self, req, resp, id):
        """Handles GET requests"""
        account = session.query(Account).filter(Account.user == req.uid, Account.id == id).first()
        if not account:
            raise HTTPNotFound(description="Account not found")
        resp.body = dumps({"status": True, "account": {
            "id": account.id,
            "iban": account.iban,
            "bic_swift": account.bic_swift,
            "currency": account.currency,
            "country": account.country
        }})


class AccountCreateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'iban' not in data or 'bic_swift' not in data or 'currency' not in data or not 'country' in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        account = Account(**data)
        account.user = req.uid
        session.add(account)
        session.commit()
        resp.body = dumps({"status": True, "account": {
            "id": account.id,
            "iban": account.iban,
            "bic_swift": account.bic_swift,
            "currency": account.currency,
            "country": account.country
        }})


class AccountUpdateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'id' not in data or 'update' not in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        account = session.query(Account).filter(Account.user == req.uid, Account.id == data['id'])
        if not account:
            raise HTTPNotFound(description="Account not found")
        account.update(data['update'])
        session.commit()
        account = account.first()
        resp.body = dumps({"status": True, "account": {
            "id": account.id,
            "iban": account.iban,
            "bic_swift": account.bic_swift,
            "currency": account.currency,
            "country": account.country
        }})


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
        session.delete(account)
        session.commit()
        resp.body = dumps({"status": True, "account": {
            "id": account.id,
            "iban": account.iban,
            "bic_swift": account.bic_swift,
            "currency": account.currency,
            "country": account.country
        }})

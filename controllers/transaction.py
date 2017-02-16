from json import load, dumps
from falcon import HTTPBadRequest, before
from middleware.token import validate_token
from models.models import Transaction, session

__all__ = ['TransactionListResource', 'TransactionGetResource',
           'TransactionCreateResource', 'TransactionDeleteResource']


class TransactionListResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        """Handles GET requests"""
        transactions = session.query(Transaction).filter(Transaction.user.id == req.id)
        output = [{
            "id": transaction.id,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "reason": transaction.reason,
            "completed": transaction.completed
        } for transaction in transactions]
        resp.body = dumps({"status": True, "transactions": output})


class TransactionGetResource(object):
    @before(validate_token)
    def on_get(self, req, resp, id):
        """Handles GET requests"""
        transaction = session.query(Transaction).get(req.uid)
        resp.body = dumps({"status": True, "transaction": {
            "id": transaction.id,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "reason": transaction.reason,
            "completed": transaction.completed
        }})


class TransactionCreateResource(object): #TODO Find bank info from IBAN
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'amount' not in data or 'currency' not in data or 'reason' not in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        transaction = Transaction(**data)
        session.add(transaction)
        session.commit()
        resp.body = dumps({"status": True, "transaction": {
            "id": transaction.id,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "reason": transaction.reason,
            "completed": transaction.completed
        }})


class TransactionDeleteResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'id' not in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        transaction = session.query(Transaction).get(req.uid)
        session.delete(transaction)
        session.commit()
        resp.body = dumps({"status": True, "transaction": {
            "id": transaction.id,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "reason": transaction.reason,
            "completed": transaction.completed
        }})

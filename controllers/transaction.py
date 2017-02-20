from json import load, dumps
from falcon import HTTPBadRequest, HTTPNotFound, before
from middleware.token import validate_token
from encoders.datetime import DateTimeEncoder
from models.models import Transaction, session
from models.schema import TransactionSchema

__all__ = ['TransactionListResource', 'TransactionGetResource',
           'TransactionCreateResource', 'TransactionDeleteResource']


class TransactionListResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        """Handles GET requests"""
        transactions = session.query(Transaction).filter(Transaction.user == req.uid)
        schema = TransactionSchema(many=True)
        resp.body = dumps({"transactions": schema.dump(transactions).data}, cls=DateTimeEncoder)


class TransactionGetResource(object):
    @before(validate_token)
    def on_get(self, req, resp, id):
        """Handles GET requests"""
        transaction = session.query(Transaction).filter(Transaction.user == req.uid, Transaction.id == id).first()
        if not transaction:
            raise HTTPNotFound(description="Transaction not found")
        schema = TransactionSchema()
        resp.body = dumps({"transaction": schema.dump(beneficiary).data}, cls=DateTimeEncoder)


class TransactionCreateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        schema = TransactionSchema()
        result = schema.load(data)
        if result.errors:
            raise HTTPBadRequest(description=result.errors)
        transaction = Transaction(**result.data)
        transaction.user = req.uid
        session.add(transaction)
        session.commit()
        result = schema.dump(transaction)
        resp.body = dumps({"transaction": result.data}, cls=DateTimeEncoder)


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
        transaction = session.query(Transaction).filter(Transaction.user == req.uid, Transaction.id == data['id']).first()
        if not transaction:
            raise HTTPNotFound(description="Transaction not found")
        session.delete(transaction)
        session.commit()
        resp.body = dumps({"status": True, "transaction": {
            "id": transaction.id,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "reason": transaction.reason,
            "completed": transaction.completed
        }})

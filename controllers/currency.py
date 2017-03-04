from json import dumps
from falcon import HTTPNotFound, before
from middleware.token import validate_token
from encoders.datetime import DateTimeEncoder
from models.models import Currency, session
from models.schema import CurrencySchema

__all__ = ['CurrencyListResource', 'CurrencyGetResource']


class CurrencyListResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        """Handles GET requests"""
        currencies = session.query(Currency)
        schema = CurrencySchema(many=True)
        resp.body = dumps({"currencies": schema.dump(currencies).data}, cls=DateTimeEncoder)


class CurrencyGetResource(object):
    @before(validate_token)
    def on_get(self, req, resp, id):
        """Handles GET requests"""
        currency = session.query(Currency).filter(Currency.id == id).first()
        if not currency:
            raise HTTPNotFound(description="Currency not found")
        schema = CurrencySchema()
        resp.body = dumps({"currency": schema.dump(currency).data}, cls=DateTimeEncoder)

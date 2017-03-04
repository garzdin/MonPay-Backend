from json import load, dumps
from falcon import HTTPNotFound, HTTPBadRequest, before
from middleware.token import validate_token
from encoders.datetime import DateTimeEncoder
from models.models import Currency, session

__all__ = ['ConversionResource']


conversions = {
    "BGN": {
        "BGN": 1,
        "EUR": 0.508561073,
        "GBP": 0.439309588,
        "DKK": 3.78076928,
        "USD": 0.540219
    },
    "EUR": {
        "EUR": 1,
        "BGN": 1.96633217,
        "GBP": 0.863828576,
        "DKK": 7.43424828,
        "USD": 1.06225
    },
    "GBP": {
        "GBP": 1,
        "EUR": 1.15763709,
        "BGN": 2.27629906,
        "DKK": 8.60616156,
        "USD": 1.2297
    },
    "DKK": {
        "DKK": 1,
        "BGN": 0.264496436,
        "EUR": 0.134512591,
        "GBP": 0.11619582,
        "USD": 0.142886
    },
    "USD": {
        "USD": 1,
        "BGN": 1.85110113,
        "EUR": 0.941397976,
        "GBP": 0.813206473,
        "DKK": 6.99858629
    }
}

fee = 0.25


class ConversionResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'from' not in data or 'to' not in data or 'amount' not in data:
            raise HTTPBadRequest(description={
                "from": "From currency is required",
                "to": "To currency is required",
                "amount": "Amount is required"
            })
        from_currency_id = data.get('from')
        to_currency_id = data.get('to')
        amount = data.get('amount')
        from_currency = session.query(Currency).get(from_currency_id)
        if not from_currency:
            raise HTTPNotFound(description="From currency not found")
        to_currency = session.query(Currency).get(to_currency_id)
        if not to_currency:
            raise HTTPNotFound(description="To currency not found")
        amount_without_fee = amount * conversions[from_currency.iso_code][to_currency.iso_code]
        fee_percent = fee / 100
        amount_with_fee = amount_without_fee + amount_without_fee * fee_percent
        conversion = {
            "from_currency": from_currency.iso_code,
            "to_currency": to_currency.iso_code,
            "from_amount": amount,
            "to_amount": amount_with_fee,
            "fee": amount_with_fee - amount_without_fee
        }
        resp.body = dumps({"conversion": conversion}, cls=DateTimeEncoder)

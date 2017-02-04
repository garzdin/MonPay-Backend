from json import load, dumps
from falcon import HTTPBadRequest, before
from currencycloud import Conversion, Reference
from middleware.token import validate_token

__all__ = ['ConversionListResource', 'ConversionGetResource',
           'ConversionCreateResource', 'ConversionDatesResource']


class ConversionListResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        """Handles GET requests"""
        beneficiaries = Conversion.find()
        output = [beneficiary.data for beneficiary in beneficiaries]
        resp.body = dumps({"status": True, "conversions": output})


class ConversionGetResource(object):
    @before(validate_token)
    def on_get(self, req, resp, id):
        """Handles GET requests"""
        conversion = Conversion.retrieve(id)
        resp.body = dumps({"status": True, "conversion": conversion.data})


class ConversionCreateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'buy_currency' not in data or 'sell_currency' not in data or 'fixed_side' not in data or 'amount' not in data or 'reason' not in data or 'term_agreement' not in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        conversion = Conversion.create(**data)
        resp.body = dumps({"status": True, "conversion": conversion.data})

class ConversionDatesResource(object):
    @before(validate_token)
    def on_get(self, req, resp, pair):
        """Handles GET requests"""
        reference = Reference.conversion_dates(conversion_pair=pair)
        output = [ref.data for ref in reference]
        resp.body = dumps({"status": True, "dates": output})

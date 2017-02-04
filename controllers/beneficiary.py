from json import load, dumps
from falcon import HTTPBadRequest, before
from currencycloud import Beneficiary, Reference
from middleware.token import validate_token
from models.models import User, session

__all__ = ['BeneficiaryListResource', 'BeneficiaryGetResource',
           'BeneficiaryCreateResource', 'BeneficiaryUpdateResource',
           'BeneficiaryDeleteResource', 'BeneficiaryDetailsResource']


class BeneficiaryListResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        """Handles GET requests"""
        beneficiaries = Beneficiary.find()
        output = [beneficiary.data for beneficiary in beneficiaries]
        resp.body = dumps({"status": True, "beneficiaries": output})


class BeneficiaryGetResource(object):
    @before(validate_token)
    def on_get(self, req, resp, id):
        """Handles GET requests"""
        beneficiary = Beneficiary.retrieve(id)
        resp.body = dumps({"status": True, "beneficiary": beneficiary.data})


class BeneficiaryCreateResource(object): #TODO Find bank info from IBAN
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'bank_account_holder_name' not in data or 'bank_country' not in data or 'currency' not in data or 'name' not in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        beneficiary = Beneficiary.create(**data)
        resp.body = dumps({"status": True, "beneficiary": beneficiary.data})


class BeneficiaryUpdateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'id' not in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        beneficiary = Beneficiary.update_id(data['id'], **data)
        resp.body = dumps({"status": True, "beneficiary": beneficiary.data})


class BeneficiaryDeleteResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'id' not in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        beneficiary = Beneficiary.delete(data)
        resp.body = dumps({"status": True, "beneficiary": beneficiary.data})


class BeneficiaryDetailsResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'beneficiary_country' not in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        reference = Reference.beneficiary_required_details(**data)
        output = [ref.data for ref in reference]
        resp.body = dumps({"status": True, "required": output})

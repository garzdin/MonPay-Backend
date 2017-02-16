from json import load, dumps
from falcon import HTTPBadRequest, before
from middleware.token import validate_token
from models.models import Beneficiary, session

__all__ = ['BeneficiaryListResource', 'BeneficiaryGetResource',
           'BeneficiaryCreateResource', 'BeneficiaryUpdateResource',
           'BeneficiaryDeleteResource']


class BeneficiaryListResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        """Handles GET requests"""
        beneficiaries = session.query(Beneficiary).filter(Beneficiary.user.id == req.id)
        output = [{
            "id": beneficiary.id,
            "first_name": beneficiary.first_name,
            "last_name": beneficiary.last_name,
            "email": beneficiary.email
        } for beneficiary in beneficiaries]
        resp.body = dumps({"status": True, "beneficiaries": output})


class BeneficiaryGetResource(object):
    @before(validate_token)
    def on_get(self, req, resp, id):
        """Handles GET requests"""
        beneficiary = session.query(Beneficiary).get(req.uid)
        resp.body = dumps({"status": True, "beneficiary": {
            "id": beneficiary.id,
            "first_name": beneficiary.first_name,
            "last_name": beneficiary.last_name,
            "email": beneficiary.email
        }})


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
        beneficiary = Beneficiary(**data)
        session.add(beneficiary)
        session.commit()
        resp.body = dumps({"status": True, "beneficiary": {
            "id": beneficiary.id,
            "first_name": beneficiary.first_name,
            "last_name": beneficiary.last_name,
            "email": beneficiary.email
        }})


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
        beneficiary = session.query(Beneficiary).get(req.uid)
        beneficiary.update(**data)
        session.commit()
        resp.body = dumps({"status": True, "beneficiary": {
            "id": beneficiary.id,
            "first_name": beneficiary.first_name,
            "last_name": beneficiary.last_name,
            "email": beneficiary.email
        }})


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
        beneficiary = session.query(Beneficiary).get(req.uid)
        session.delete(beneficiary)
        session.commit()
        resp.body = dumps({"status": True, "beneficiary": {
            "id": beneficiary.id,
            "first_name": beneficiary.first_name,
            "last_name": beneficiary.last_name,
            "email": beneficiary.email
        }})

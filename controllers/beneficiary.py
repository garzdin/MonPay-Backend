from json import load, dumps
from falcon import HTTPBadRequest, HTTPNotFound, before
from middleware.token import validate_token
from models.models import Beneficiary, session

__all__ = ['BeneficiaryListResource', 'BeneficiaryGetResource',
           'BeneficiaryCreateResource', 'BeneficiaryUpdateResource',
           'BeneficiaryDeleteResource']


class BeneficiaryListResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        """Handles GET requests"""
        beneficiaries = session.query(Beneficiary).filter(Beneficiary.user == req.uid)
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
        beneficiary = session.query(Beneficiary).filter(Beneficiary.user == req.uid, Beneficiary.id == id).first()
        if not beneficiary:
            raise HTTPNotFound(description="Beneficiary not found")
        resp.body = dumps({"status": True, "beneficiary": {
            "id": beneficiary.id,
            "first_name": beneficiary.first_name,
            "last_name": beneficiary.last_name,
            "email": beneficiary.email
        }})


class BeneficiaryCreateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'first_name' not in data or 'last_name' not in data:
            raise HTTPBadRequest(
                description="Provide all required fields")
        beneficiary = Beneficiary(**data)
        beneficiary.user = req.uid
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
        if 'id' not in data or 'update' not in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        beneficiary = session.query(Beneficiary).filter(Beneficiary.user == req.uid, Beneficiary.id == data['id'])
        if not beneficiary:
            raise HTTPNotFound(description="Beneficiary not found")
        beneficiary.update(data['update'])
        session.commit()
        beneficiary = beneficiary.first()
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
        beneficiary = session.query(Beneficiary).filter(Beneficiary.user == req.uid, Beneficiary.id == data['id']).first()
        if not beneficiary:
            raise HTTPNotFound(description="Beneficiary not found")
        session.delete(beneficiary)
        session.commit()
        resp.body = dumps({"status": True, "beneficiary": {
            "id": beneficiary.id,
            "first_name": beneficiary.first_name,
            "last_name": beneficiary.last_name,
            "email": beneficiary.email
        }})

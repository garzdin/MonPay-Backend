from json import load, dumps
from datetime import datetime
from falcon import HTTPBadRequest, HTTPConflict, HTTPNotFound, HTTPForbidden, before
from currencycloud import Beneficiary
from middleware.token import validate_token
from models.models import User, session

__all__ = ['BeneficiaryListResource', 'BeneficiaryGetResource',
           'BeneficiaryCreateResource', 'BeneficiaryUpdateResource',
           'BeneficiaryDeleteResource']


def BeneficiaryListResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        """Handles GET requests"""
        beneficiaries = Beneficiary.find()
        resp.body = dumps({"status": True, "beneficiaries": beneficiaries})


def BeneficiaryGetResource(object):
    @before(validate_token)
    def on_get(self, req, resp, id):
        """Handles GET requests"""
        beneficiary = Beneficiary.retrieve(id)
        resp.body = dumps({"status": True, "beneficiary": beneficiary})


def BeneficiaryCreateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'bank_account_holder_name' not in data or 'bank_country' not in data or 'currency' not in data or 'name' not in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        beneficiary = Beneficiary.create(data)
        resp.body = dumps({"status": True, "beneficiary": beneficiary})


def BeneficiaryUpdateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if 'id' not in data:
            raise HTTPBadRequest(
                description="Provide all needed required fields")
        beneficiary = Beneficiary.update(data)
        resp.body = dumps({"status": True, "beneficiary": beneficiary})


def BeneficiaryDeleteResource(object):
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
        resp.body = dumps({"status": True, "beneficiary": beneficiary})

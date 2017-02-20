from json import load, dumps
from falcon import HTTPBadRequest, HTTPNotFound, before
from middleware.token import validate_token
from encoders.datetime import DateTimeEncoder
from models.models import Beneficiary, session
from models.schema import BeneficiarySchema

__all__ = ['BeneficiaryListResource', 'BeneficiaryGetResource',
           'BeneficiaryCreateResource', 'BeneficiaryUpdateResource',
           'BeneficiaryDeleteResource']


class BeneficiaryListResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        """Handles GET requests"""
        beneficiaries = session.query(Beneficiary).filter(Beneficiary.user == req.uid)
        schema = BeneficiarySchema(many=True)
        resp.body = dumps({"beneficiaries": schema.dump(beneficiaries).data}, cls=DateTimeEncoder)


class BeneficiaryGetResource(object):
    @before(validate_token)
    def on_get(self, req, resp, id):
        """Handles GET requests"""
        beneficiary = session.query(Beneficiary).filter(Beneficiary.user == req.uid, Beneficiary.id == id).first()
        if not beneficiary:
            raise HTTPNotFound(description="Beneficiary not found")
        schema = BeneficiarySchema()
        resp.body = dumps({"beneficiary": schema.dump(beneficiary).data}, cls=DateTimeEncoder)


class BeneficiaryCreateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        schema = BeneficiarySchema()
        result = schema.load(data)
        if result.errors:
            raise HTTPBadRequest(description=result.errors)
        beneficiary = Beneficiary(**result.data)
        beneficiary.user = req.uid
        session.add(beneficiary)
        session.commit()
        result = schema.dump(beneficiary)
        resp.body = dumps({"beneficiary": result.data}, cls=DateTimeEncoder)


class BeneficiaryUpdateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        beneficiary = session.query(Beneficiary).filter(Beneficiary.user == req.uid, Beneficiary.id == data['id'])
        if not beneficiary:
            raise HTTPNotFound(description="Beneficiary not found")
        schema = BeneficiarySchema()
        result = schema.load(data)
        if result.errors:
            raise HTTPBadRequest(description=result.errors)
        beneficiary.update(result.data)
        session.commit()
        result = schema.dump(beneficiary.first())
        resp.body = dumps({"beneficiary": result.data}, cls=DateTimeEncoder)


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

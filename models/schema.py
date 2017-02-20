from marshmallow import Schema, fields

class Id(object):
    id = fields.Integer()


class Version(object):
    created_on = fields.DateTime()
    updated_on = fields.DateTime()
    version = fields.Integer()


class Identity(object):
    id_type = fields.Integer()
    id_value = fields.Str()


class Entity(object):
    entity_type = fields.Integer()
    first_name = fields.Str()
    last_name = fields.Str()
    date_of_birth = fields.Date()


class UserSchema(Schema, Id, Entity, Identity, Version):
    email = fields.Str()
    password = fields.Str()
    address = fields.Nested('AddressSchema')
    is_admin = fields.Boolean()
    accounts = fields.Nested('AccountSchema', many=True)
    beneficiaries = fields.Nested('BeneficiarySchema', many=True)
    transactions = fields.Nested('TransactionSchema', many=True)


class BeneficiarySchema(Schema, Id, Entity, Identity, Version):

    email = fields.Str()
    address = fields.Nested('AddressSchema')
    user = fields.Integer()
    accounts = fields.Nested('AccountSchema', many=True)
    transactions = fields.Nested('TransactionSchema', many=True)


class AccountSchema(Schema, Id, Version):
    iban = fields.Str()
    bic_swift = fields.Str()
    currency = fields.Str()
    country = fields.Str()
    user = fields.Integer()
    beneficiary = fields.Integer()
    transactions = fields.Nested('TransactionSchema', many=True)


class TransactionSchema(Schema, Id, Version):
    reference = fields.Str()
    amount = fields.Float()
    currency = fields.Str()
    reason = fields.Str()
    completed = fields.Boolean()
    user = fields.Integer()
    beneficiary = fields.Integer()
    account = fields.Integer()


class AddressSchema(Schema, Id, Version):
    address = fields.Str()
    city = fields.Str()
    state_or_province = fields.Str()
    postal_code = fields.Integer()
    country = fields.Str()
    user_id = fields.Integer()
    user = fields.Nested('UserSchema')
    beneficiary_id = fields.Integer()
    beneficiary = fields.Nested('BeneficiarySchema')

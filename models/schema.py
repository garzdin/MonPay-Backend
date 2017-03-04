from marshmallow import Schema, fields

__all__ = ['UserSchema', 'BeneficiarySchema', 'AccountSchema',
           'TransactionSchema', 'AddressSchema']


class Id(object):
    id = fields.Integer()


class Entity(object):
    entity_type = fields.Integer(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)


class Birth(object):
    date_of_birth = fields.Date(required=True)

class Phone(object):
    phone_number = fields.Str()

class Identity(object):
    id_type = fields.Integer()
    id_value = fields.Str()


class Version(object):
    created_on = fields.DateTime(dump_only=True)
    updated_on = fields.DateTime(dump_only=True)
    version = fields.Integer(dump_only=True)


class UserSchema(Schema, Id, Entity, Birth, Phone, Identity, Version):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    address = fields.Nested('AddressSchema')
    is_admin = fields.Boolean(default=False)
    accounts = fields.Nested('AccountSchema', many=True)
    beneficiaries = fields.Nested('BeneficiarySchema', many=True)
    transactions = fields.Nested('TransactionSchema', many=True)


class BeneficiarySchema(Schema, Id, Entity, Phone, Identity, Version):
    email = fields.Email(required=True)
    user = fields.Integer()
    account = fields.Nested('AccountSchema')
    transactions = fields.Nested('TransactionSchema', many=True)


class AccountSchema(Schema, Id, Version):
    iban = fields.Str(required=True)
    bic_swift = fields.Str()
    currency = fields.Integer()
    country = fields.Str(required=True)
    active = fields.Boolean(default=False)
    user = fields.Integer()
    beneficiary = fields.Integer()
    transactions = fields.Nested('TransactionSchema', many=True)


class CurrencySchema(Schema, Id, Version):
    iso_code = fields.Str(required=True)
    display_name = fields.Str()
    accounts = fields.Nested('AccountSchema', many=True)
    transactions = fields.Nested('TransactionSchema', many=True)


class TransactionSchema(Schema, Id, Version):
    reference = fields.Str()
    amount = fields.Float(required=True)
    currency = fields.Integer()
    reason = fields.Str(required=True)
    completed = fields.Boolean(default=False)
    user = fields.Integer()
    beneficiary = fields.Integer()
    account = fields.Integer()


class AddressSchema(Schema, Id, Version):
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    state_or_province = fields.Str()
    postal_code = fields.Integer(required=True)
    country = fields.Str(required=True)
    user = fields.Integer()

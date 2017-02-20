from marshmallow import Schema, fields

__all__ = ['UserSchema', 'BeneficiarySchema', 'AccountSchema',
           'TransactionSchema', 'AddressSchema']


class Id(object):
    id = fields.Integer()


class Version(object):
    created_on = fields.DateTime(dump_only=True)
    updated_on = fields.DateTime(dump_only=True)
    version = fields.Integer(dump_only=True)


class Identity(object):
    id_type = fields.Integer()
    id_value = fields.Str()


class Entity(object):
    entity_type = fields.Integer(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    date_of_birth = fields.Date(required=True)


class Phone(object):
    phone_number = field.Str()


class UserSchema(Schema, Id, Entity, Identity, Version, Phone):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    address = fields.Nested('AddressSchema')
    is_admin = fields.Boolean(default=False)
    accounts = fields.Nested('AccountSchema', many=True)
    beneficiaries = fields.Nested('BeneficiarySchema', many=True)
    transactions = fields.Nested('TransactionSchema', many=True)


class BeneficiarySchema(Schema, Id, Entity, Identity, Version, Phone):
    email = fields.Email(required=True)
    address = fields.Nested('AddressSchema')
    user = fields.Integer()
    accounts = fields.Nested('AccountSchema', many=True)
    transactions = fields.Nested('TransactionSchema', many=True)


class AccountSchema(Schema, Id, Version):
    iban = fields.Str(required=True)
    bic_swift = fields.Str()
    currency = fields.Str(required=True)
    country = fields.Str(required=True)
    user = fields.Integer()
    beneficiary = fields.Integer()
    transactions = fields.Nested('TransactionSchema', many=True)


class TransactionSchema(Schema, Id, Version):
    reference = fields.Str()
    amount = fields.Float(required=True)
    currency = fields.Str(required=True)
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
    user_id = fields.Integer()
    user = fields.Nested('UserSchema')
    beneficiary_id = fields.Integer()
    beneficiary = fields.Nested('BeneficiarySchema')

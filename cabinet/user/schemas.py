from marshmallow import Schema, fields


class UserInputSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class UserSchema(Schema):
    id = fields.Integer(required=True)
    username = fields.String(required=True)
    # TODO add roles
    created_on = fields.Time(required=True)
    updated_on = fields.Time(required=True)


user_schema = UserSchema()
user_list_schema = UserSchema(many=True)
user_input_schema = UserInputSchema()

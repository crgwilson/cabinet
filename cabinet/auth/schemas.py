from marshmallow import Schema, fields


class PermissionOutputSchema(Schema):
    id = fields.Integer(required=True)

    name = fields.String(required=True)
    description = fields.String(required=True)

    created_on = fields.Time(required=True)
    updated_on = fields.Time(required=True)


class RoleOutputSchema(Schema):
    id = fields.Integer(required=True)

    name = fields.String(required=True)
    description = fields.String(required=True)

    permissions = fields.Nested(lambda: PermissionOutputSchema(only=["id"]))

    created_on = fields.Time(required=True)
    updated_on = fields.Time(required=True)


class LoginInputSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class LoginOutputSchema(Schema):
    token = fields.String(required=True)


permission_schema = PermissionOutputSchema()
permission_list_schema = PermissionOutputSchema(many=True)
role_schema = RoleOutputSchema()
role_list_schema = RoleOutputSchema(many=True)
login_input_schema = LoginInputSchema()
login_output_schema = LoginOutputSchema()

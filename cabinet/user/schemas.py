from marshmallow import Schema, fields

from cabinet.auth.schemas import RoleOutputSchema


class UserInputSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class UserOutputSchema(Schema):
    id = fields.Integer(required=True)
    username = fields.String(required=True)

    roles: fields.List = fields.List(
        fields.Nested(lambda: RoleOutputSchema(only=["id"]))  # type: ignore
    )

    created_on = fields.DateTime(required=True)
    updated_on = fields.DateTime(required=True)


user_schema = UserOutputSchema()
user_list_schema = UserOutputSchema(many=True)
user_input_schema = UserInputSchema()

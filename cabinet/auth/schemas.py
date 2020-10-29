from marshmallow import Schema, fields


class PermissionSchema(Schema):
    id = fields.Integer(required=True)

    name = fields.String(required=True)
    description = fields.String(required=True)

    created_on = fields.Time(required=True)
    updated_on = fields.Time(required=True)


class RoleSchema(Schema):
    id = fields.Integer(required=True)

    name = fields.String(required=True)
    description = fields.String(required=True)

    permissions = fields.Nested(lambda: PermissionSchema(only=["id"]))

    created_on = fields.Time(required=True)
    updated_on = fields.Time(required=True)


permission_schema = PermissionSchema()
permission_list_schema = PermissionSchema(many=True)
role_schema = RoleSchema()
role_list_schema = RoleSchema(many=True)

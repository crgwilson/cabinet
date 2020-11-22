from cabinet.database import db

role_permission_association = db.Table(
    "role_permission_association",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id")),
)

user_role_association = db.Table(
    "user_role_association",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
)

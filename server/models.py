from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from server.config import db, bcrypt
from marshmallow import Schema, fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)
    recipes = db.relationship('Recipe', backref='user', cascade='all, delete-orphan')

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Marshmallow schemas
class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    image_url = fields.Str()
    bio = fields.Str()

class RecipeSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    instructions = fields.Str()
    minutes_to_complete = fields.Int()
    user = fields.Nested(UserSchema)

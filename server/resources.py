from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from server.config import db
from server.models import User, Recipe, UserSchema, RecipeSchema


class Signup(Resource):
    def post(self):
        data = request.get_json()
        user = User(
            username=data['username'],
            password=data['password'],
            image_url=data.get('image_url'),
            bio=data.get('bio', '')
        )
        db.session.add(user)
        try:
            db.session.commit()
            return UserSchema().dump(user), 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Username already exists'}, 400


class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            return UserSchema().dump(user), 200
        return {'error': 'Not authenticated'}, 401


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        if user and user.authenticate(data.get('password')):
            session['user_id'] = user.id
            return UserSchema().dump(user), 200
        return {'error': 'Invalid credentials'}, 401


class Logout(Resource):
    def delete(self):
        if 'user_id' in session:
            session.pop('user_id')
            return {'message': 'Logged out successfully'}, 200
        return {'error': 'Not logged in'}, 401


class RecipeIndex(Resource):
    def get(self):
        recipes = Recipe.query.all()
        return RecipeSchema(many=True).dump(recipes), 200

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Not authenticated'}, 401

        data = request.get_json()
        recipe = Recipe(
            user_id=user_id,
            title=data['title'],
            instructions=data['instructions'],
            minutes_to_complete=data['minutes_to_complete']
        )
        db.session.add(recipe)
        db.session.commit()
        return RecipeSchema().dump(recipe), 201

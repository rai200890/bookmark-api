from flask_restful import Resource
from webargs.flaskparser import use_kwargs

from bookmark_api import db
from bookmark_api.models import User

from bookmark_api.resources.schemas import (
    UserListResponseSchema,
    CreateUserRequestSchema,
    EditUserRequestSchema,
    UserResponseSchema
)


class UserListResource(Resource):

    def get(self):
        users = User.query.all()
        return UserListResponseSchema().dump(users)


class UserResource(Resource):

    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return UserResponseSchema().dump(user).data

    @use_kwargs(CreateUserRequestSchema)
    def post(self, **kwargs):
        try:
            password = kwargs['user'].pop('password', None)
            user = User(**kwargs['user'])
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            return UserResponseSchema().dump(user).data
        except Exception as e:
            return {'errors': e.args}, 422

    def delete(self, user_id):
        deleted_records = User.query.filter_by(id=user_id).delete()
        if deleted_records > 0:
            return None, 204
        return None, 422

    @use_kwargs(EditUserRequestSchema)
    def put(self, user_id, **kwargs):
        try:
            user = User.query.filter_by(id=user_id).first()
            password = kwargs['user'].pop('password', None)
            for attribute, value in kwargs['user'].items():
                setattr(user, attribute, value)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            return None, 204
        except Exception as e:
            return {'errors': e.args}, 422

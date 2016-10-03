from flask_restful import Resource
from webargs.flaskparser import use_kwargs
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from bookmark_api import db
from bookmark_api.models import User
from bookmark_api.resources.schemas import (
    UserListResponseSchema,
    CreateUserRequestSchema,
    EditUserRequestSchema,
    UserResponseSchema
)
from bookmark_api.permission import (
    requires_permission,
    admin_permission,
    ViewUserPermission,
    EditUserPermission,
    DeleteUserPermission
)
from bookmark_api.resources.common import assign_attributes


class UserListResource(Resource):

    @jwt_required()
    @admin_permission.require()
    def get(self):
        users = User.query.all()
        return UserListResponseSchema().dump(users)


class UserResource(Resource):

    @jwt_required()
    @requires_permission(permission_class=ViewUserPermission, field='user_id')
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return UserResponseSchema().dump(user).data

    @jwt_required()
    @use_kwargs(CreateUserRequestSchema)
    def post(self, **kwargs):
        try:
            password = kwargs['user'].pop('password', None)
            user = User(**kwargs['user'])
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            return UserResponseSchema().dump(user).data
        except SQLAlchemyError as e:
            return {'errors': e.args}, 422

    @jwt_required()
    @requires_permission(permission_class=DeleteUserPermission, field='user_id')
    @admin_permission.require()
    def delete(self, user_id):
        deleted_records = User.query.filter_by(id=user_id).delete()
        if deleted_records > 0:
            return None, 204
        return None, 422

    @jwt_required()
    @requires_permission(permission_class=EditUserPermission, field='user_id')
    @use_kwargs(EditUserRequestSchema)
    def put(self, user_id, **kwargs):
        try:
            user = User.query.filter_by(id=user_id).first()
            password = kwargs['user'].pop('password', None)
            if user.role.name == 'client':
                kwargs['user'].pop('role_id', None)
            assign_attributes(user, kwargs['user'])
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            return None, 204
        except SQLAlchemyError as e:
            return {'errors': e.args}, 422

from flask_restful import Resource
from webargs.flaskparser import use_kwargs
from flask_jwt import jwt_required, current_identity
from sqlalchemy.exc import SQLAlchemyError

from bookmark_api import db
from bookmark_api.models import User
from bookmark_api.resources.schemas import (
    UserListResponseSchema,
    CreateUserRequestSchema,
    EditUserRequestSchema,
    UserResponseSchema
)
from bookmark_api.authorization import (
    requires_permission,
    admin_permission,
    ViewUserPermission,
    EditUserPermission,
    DeleteUserPermission
)
from bookmark_api.resources.common import (
    assign_attributes,
    handle_delete
)
from bookmark_api.models import Role
from bookmark_api import cache


class UserListResource(Resource):

    @jwt_required()
    @admin_permission.require()
    def get(self):
        users = User.query.all()
        return UserListResponseSchema().dump(users)


class UserResource(Resource):

    @cache.cached()
    @jwt_required()
    @requires_permission(permission_class=ViewUserPermission, field='user_id')
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return UserResponseSchema().dump(user).data

    @use_kwargs(CreateUserRequestSchema)
    def post(self, **kwargs):
        try:
            user = User()
            self._assign_attributes(user, kwargs['user'])
            db.session.add(user)
            db.session.commit()
            return UserResponseSchema().dump(user).data
        except SQLAlchemyError as e:
            return {'errors': e.args}, 422

    @jwt_required()
    @requires_permission(permission_class=DeleteUserPermission, field='user_id')
    def delete(self, user_id):
        return handle_delete(User, user_id)

    @jwt_required()
    @requires_permission(permission_class=EditUserPermission, field='user_id')
    @use_kwargs(EditUserRequestSchema)
    def put(self, user_id, **kwargs):
        try:
            user = User.query.filter_by(id=user_id).first()
            self._assign_attributes(user, kwargs['user'])
            db.session.add(user)
            db.session.commit()
            return None, 204
        except SQLAlchemyError as e:
            return {'errors': e.args}, 422

    @staticmethod
    def _assign_attributes(instance, params):
        role_id = Role.query.filter_by(name='client').first().id
        if current_identity and current_identity.role.name == 'admin':
            role_id = params.pop('role_id', None)
        params.update({"role_id": role_id})
        password = params.pop('password', None)
        if password is not None:
            instance.hash_password(password)
        assign_attributes(instance, params)

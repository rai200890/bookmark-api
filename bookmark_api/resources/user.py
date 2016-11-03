from flask.views import MethodView
from flask import jsonify
from webargs.flaskparser import use_kwargs
from flask_jwt import jwt_required, current_identity
from sqlalchemy.exc import SQLAlchemyError

from bookmark_api import db
from bookmark_api.models import User
from bookmark_api.resources.schemas import (
    UserListResponseSchema,
    CreateUserRequestSchema,
    EditUserRequestSchema,
    UserResponseSchema,
    RoleListResponseSchema
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


class RoleListResource(MethodView):

    @jwt_required()
    @admin_permission.require()
    def get(self):
        roles = Role.query.all()
        return RoleListResponseSchema().dumps(roles).data, 200


class UserListResource(MethodView):

    @jwt_required()
    @admin_permission.require()
    def get(self):
        users = User.query.all()
        return UserListResponseSchema().dumps(users).data, 200


class UserResource(MethodView):

    @cache.cached()
    @jwt_required()
    @requires_permission(permission_class=ViewUserPermission, field='user_id')
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return UserResponseSchema().dumps(user).data, 200

    @use_kwargs(CreateUserRequestSchema)
    def post(self, **kwargs):
        try:
            user = User()
            self._assign_attributes(user, kwargs['user'])
            db.session.add(user)
            db.session.commit()
            return UserResponseSchema().dumps(user).data, 200
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
            return ('', 204)
        except SQLAlchemyError as e:
            return jsonify({'errors': e.args}), 422

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

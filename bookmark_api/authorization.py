from collections import namedtuple
from functools import partial, wraps

from flask import abort
from flask_principal import (
    Permission,
    RoleNeed
)
from bookmark_api.models import (
    User,
    Bookmark
)


BookmarkNeed = namedtuple('bookmark', ['method', 'value'])
UserNeed = namedtuple('user', ['method', 'value'])

ViewBookmarkNeed = partial(BookmarkNeed, 'view')
DeleteBookmarkNeed = partial(BookmarkNeed, 'delete')
EditBookmarkNeed = partial(BookmarkNeed, 'edit')

ViewUserNeed = partial(UserNeed, 'view')
DeleteUserNeed = partial(UserNeed, 'delete')
EditUserNeed = partial(UserNeed, 'edit')


class ViewBookmarkPermission(Permission):
    def __init__(self, id):
        need = ViewBookmarkNeed(id)
        super(ViewBookmarkPermission, self).__init__(need)


class DeleteBookmarkPermission(Permission):
    def __init__(self, id):
        need = ViewBookmarkNeed(id)
        super(DeleteBookmarkPermission, self).__init__(need)


class EditBookmarkPermission(Permission):
    def __init__(self, id):
        need = EditBookmarkNeed(id)
        super(EditBookmarkPermission, self).__init__(need)


class ViewUserPermission(Permission):
    def __init__(self, id):
        need = ViewUserNeed(id)
        super(ViewUserPermission, self).__init__(need)


class DeleteUserPermission(Permission):
    def __init__(self, id):
        need = DeleteUserNeed(id)
        super(DeleteUserPermission, self).__init__(need)


class EditUserPermission(Permission):
    def __init__(self, id):
        need = EditUserNeed(id)
        super(EditUserPermission, self).__init__(need)


admin_permission = Permission(RoleNeed('admin'))
client_permission = Permission(RoleNeed('client'))


def requires_permission(**params):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            id = kwargs[params['field']]
            permission = params['permission_class'](id)
            if permission.can():
                return f(*args, **kwargs)
            return abort(403)
        return wrapped
    return wrapper


def provide_permissions(identity):
    user = identity.user
    role_name = user.role.name
    identity.provides.add(RoleNeed(role_name))
    if role_name == 'client':
        for bookmark in user.bookmarks:
            for need_class in [ViewBookmarkNeed, DeleteBookmarkNeed, EditBookmarkNeed]:
                identity.provides.add(need_class(bookmark.id))
        identity.provides.add(ViewUserNeed(user.id))
        identity.provides.add(EditUserNeed(user.id))
    elif role_name == 'admin':
        for bookmark in Bookmark.query.all():
            identity.provides.add(ViewBookmarkNeed(bookmark.id))
        for user in User.query.all():
            for need_class in [ViewUserNeed, EditUserNeed, DeleteUserNeed]:
                identity.provides.add(need_class(user.id))

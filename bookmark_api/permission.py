from flask_principal import (
    Permission,
    RoleNeed
)
from collections import namedtuple
from functools import partial


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

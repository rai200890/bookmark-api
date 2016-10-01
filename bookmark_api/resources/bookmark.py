from functools import wraps

from flask import abort
from flask_restful import Resource
from webargs.flaskparser import use_kwargs
from flask_jwt import jwt_required, current_identity
from sqlalchemy.exc import SQLAlchemyError

from bookmark_api import db
from bookmark_api.models import Bookmark

from bookmark_api.resources.schemas import (
    BookmarkListRequestSchema,
    BookmarkListResponseSchema,
    CreateBookmarkRequestSchema,
    EditBookmarkRequestSchema,
    BookmarkResponseSchema
)


from bookmark_api.permission import (
    client_permission,
    ViewBookmarkPermission,
    EditBookmarkPermission,
    DeleteBookmarkPermission
)


def requires_permission(permission_klass):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            permission = permission_klass(kwargs["bookmark_id"])
            if permission.can():
                return f(*args, **kwargs)
            return abort(403)
        return wrapped
    return wrapper


class BookmarkListResource(Resource):

    @jwt_required()
    @use_kwargs(BookmarkListRequestSchema)
    def get(self, **kwargs):
        if current_identity.role.name == 'admin':
            bookmarks = Bookmark.query.group_by(Bookmark.user_id).paginate(**kwargs)
        else:
            bookmarks = Bookmark.query.filter_by(user_id=current_identity.id).paginate(**kwargs)
        return BookmarkListResponseSchema().dump(bookmarks)


class BookmarkResource(Resource):

    @jwt_required()
    @requires_permission(ViewBookmarkPermission)
    def get(self, bookmark_id):
        bookmark = Bookmark.query.get_or_404(bookmark_id)
        return BookmarkResponseSchema().dump(bookmark).data

    @jwt_required()
    @client_permission.require()
    @use_kwargs(CreateBookmarkRequestSchema)
    def post(self, **kwargs):
        try:
            params = kwargs['bookmark']
            params.update({"user_id": current_identity.id})
            bookmark = Bookmark(**params)
            db.session.add(bookmark)
            db.session.commit()
            return BookmarkResponseSchema().dump(bookmark).data
        except SQLAlchemyError as e:
            return {'errors': e.args}, 422

    @jwt_required()
    @requires_permission(DeleteBookmarkPermission)
    def delete(self, bookmark_id):
        deleted_records = Bookmark.query.filter_by(id=bookmark_id).delete()
        if deleted_records > 0:
            return None, 204
        return None, 422

    @jwt_required()
    @requires_permission(EditBookmarkPermission)
    @use_kwargs(EditBookmarkRequestSchema)
    def put(self, bookmark_id, **kwargs):
        try:
            bookmark = Bookmark.query.filter_by(id=bookmark_id).first()
            for attribute, value in kwargs['bookmark'].items():
                setattr(bookmark, attribute, value)
            db.session.commit()
            return None, 204
        except SQLAlchemyError as e:
            return {'errors': e.args}, 422

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


class BookmarkListResource(Resource):

    @jwt_required()
    @use_kwargs(BookmarkListRequestSchema)
    def get(self, **kwargs):
        bookmarks = Bookmark.query.paginate(**kwargs)
        return BookmarkListResponseSchema().dump(bookmarks)


class BookmarkResource(Resource):

    @jwt_required()
    def get(self, bookmark_id):
        bookmark = Bookmark.query.get_or_404(bookmark_id)
        return BookmarkResponseSchema().dump(bookmark).data

    @jwt_required()
    @use_kwargs(CreateBookmarkRequestSchema)
    def post(self, **kwargs):
        try:
            params = kwargs['bookmark']
            params["user_id"] = current_identity.id
            bookmark = Bookmark(**params)
            db.session.add(bookmark)
            db.session.commit()
            return BookmarkResponseSchema().dump(bookmark).data
        except SQLAlchemyError as e:
            return {'errors': e.args}, 422

    @jwt_required()
    def delete(self, bookmark_id):
        deleted_records = Bookmark.query.filter_by(id=bookmark_id).delete()
        if deleted_records > 0:
            return None, 204
        return None, 422

    @jwt_required()
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

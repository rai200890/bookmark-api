from flask_restful import Resource
from webargs.flaskparser import use_kwargs

from bookmark_api import db
from bookmark_api.models import Bookmark

from bookmark_api.resources.schemas import (
    BookmarkListRequestSchema,
    BookmarkListResponseSchema,
    BookmarkRequestSchema,
    BookmarkResponseSchema
)


class BookmarkListResource(Resource):

    @use_kwargs(BookmarkListRequestSchema)
    def get(self, **kwargs):
        bookmarks = Bookmark.query.paginate(**kwargs)
        return BookmarkListResponseSchema().dump(bookmarks)


class BookmarkResource(Resource):

    def get(self, bookmark_id):
        bookmark = Bookmark.query.get_or_404(bookmark_id)
        return BookmarkResponseSchema().dump(bookmark).data

    @use_kwargs(BookmarkRequestSchema)
    def post(self, **kwargs):
        try:
            bookmark = Bookmark(**kwargs['bookmark'])
            db.session.add(bookmark)
            db.session.commit()
            return BookmarkResponseSchema().dump(bookmark).data
        except Exception as e:
            return {'errors': e.args}, 422

    def delete(self, bookmark_id):
        deleted_records = Bookmark.query.filter_by(id=bookmark_id).delete()
        if deleted_records > 0:
            return None, 204
        return None, 422

    @use_kwargs(BookmarkRequestSchema)
    def put(self, bookmark_id, **kwargs):
        updated_records = Bookmark.query.filter_by(id=bookmark_id).update(kwargs["bookmark"])
        if updated_records > 0:
            return None, 204
        return None, 422

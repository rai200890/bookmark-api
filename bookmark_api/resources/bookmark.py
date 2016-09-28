from flask_restful import Resource
from webargs.flaskparser import use_args, use_kwargs
from sqlalchemy.exc import IntegrityError

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

    @use_args(BookmarkRequestSchema)
    def post(self, args):
        try:
            bookmark = Bookmark(**args['bookmark'])
            db.session.add(bookmark)
            result = db.session.commit()
            return BookmarkResponseSchema().dump(bookmark).data
        except Exception as e:
            return {'errors': e.args}, 422

    def delete(self, bookmark_id):
        deleted_records = Bookmark.query.filter_by(id=bookmark_id).delete()
        if deleted_records > 0:
            return None, 204
        return None, 422

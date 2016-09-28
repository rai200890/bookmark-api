from flask_restful import Resource
from webargs.flaskparser import use_kwargs

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
        bookmark = Bookmark(**kwargs['bookmark'])
        return BookmarkResponseSchema().dump(bookmark).data

    def delete(self, bookmark_id):
        deleted_records = Bookmark.query.filter_by(id=bookmark_id).delete()
        if deleted_records > 0:
            return None, 204
        return None, 422

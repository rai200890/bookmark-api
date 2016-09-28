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
        bookmark = Bookmark.create(**kwargs)
        return BookmarkResponseSchema().dump(bookmark).data

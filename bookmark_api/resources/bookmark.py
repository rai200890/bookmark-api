from flask_restful import Resource
from webargs.flaskparser import use_kwargs

from bookmark_api.models import Bookmark

from bookmark_api.resources.schemas import BookmarkListRequestSchema


class BookmarkListResource(Resource):

    @use_kwargs(BookmarkListRequestSchema)
    def get(self, **kwargs):
        bookmarks = Bookmark.query.all()
        return {"bookmarks": {"id": 1, "title": "", "url": ""}}

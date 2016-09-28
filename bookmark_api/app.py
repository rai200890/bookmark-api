from bookmark_api import app, db, api
from bookmark_api.resources.bookmark import (
    BookmarkListResource,
    BookmarkResource
)


api.add_resource(BookmarkListResource, '/bookmarks', endpoint='bookmark_list')
api.add_resource(BookmarkResource, '/bookmarks/<int:bookmark_id>', endpoint='bookmark_details')


@app.route("/healthcheck")
def healthcheck():
    result = db.engine.execute("SELECT 1;").fetchone()
    return "DB: OK {}".format(result)

if __name__ == "__main__":
    app.run()

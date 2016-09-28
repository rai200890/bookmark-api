from bookmark_api import app, db, api
from bookmark_api.resources.bookmark import (
    BookmarkListResource,
    BookmarkResource
)
from flask import jsonify


api.add_resource(BookmarkListResource, '/bookmarks')
api.add_resource(BookmarkResource, '/bookmarks', '/bookmarks/<bookmark_id>')


@app.route("/healthcheck")
def healthcheck():
    result = db.engine.execute("SELECT 1;").fetchone()
    return "DB: OK {}".format(result)


@app.errorhandler(422)
def handle_unprocessable_entity(err):

    data = getattr(err, 'data')
    if data:
        messages = data['exc'].messages
    else:
        messages = [err.args]
    return jsonify({"errors": messages}), 422


if __name__ == "__main__":
    app.run()

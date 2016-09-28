from flask import jsonify

from bookmark_api import app, db, api
from bookmark_api.resources.bookmark import (
    BookmarkListResource,
    BookmarkResource
)
from bookmark_api.resources.user import (
    UserListResource,
    UserResource
)


api.add_resource(BookmarkListResource, "/bookmarks", endpoint="bookmark_list")
api.add_resource(BookmarkResource, "/bookmarks", "/bookmarks/<int:bookmark_id>", endpoint="bookmark")
api.add_resource(UserListResource, "/users", endpoint="user_list")
api.add_resource(UserResource, "/users", "/users/<int:user_id>", endpoint="user")


@app.route("/healthcheck")
def healthcheck():
    result = db.engine.execute("SELECT 1;").fetchone()
    return "DB: OK {}".format(result)


@app.errorhandler(422)
def handle_unprocessable_entity(err):
    data = getattr(err, "data")
    if data:
        messages = data["exc"].messages
    else:
        messages = [err.args]
    return jsonify({"errors": messages}), 422


if __name__ == "__main__":
    app.run()

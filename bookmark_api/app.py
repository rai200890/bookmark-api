from flask import jsonify
from flask_jwt import JWT
from flask_principal import (
    Principal,
    Identity,
    AnonymousIdentity,
    identity_changed,
    identity_loaded,
    PermissionDenied
)

from bookmark_api import app, db, api
from bookmark_api.models import User
from bookmark_api.resources.bookmark import (
    BookmarkListResource,
    BookmarkResource
)
from bookmark_api.resources.user import (
    UserListResource,
    UserResource
)
from bookmark_api.authorization import provide_permissions


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        identity_changed.send(app,
                              identity=Identity(user.id))
        return user
    else:
        identity_changed.send(app,
                              identity=AnonymousIdentity())


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    user = User.query.filter_by(id=identity.id).one()
    identity.user = user
    provide_permissions(identity)


jwt = JWT(app, authenticate, identity)

principal = Principal(app)

# API ENDPOINTS
api.add_resource(BookmarkListResource, "/bookmarks", endpoint="bookmark_list")
api.add_resource(BookmarkResource, "/bookmarks", "/bookmarks/<int:bookmark_id>", endpoint="bookmark")
api.add_resource(UserListResource, "/users", endpoint="user_list")
api.add_resource(UserResource, "/users", "/users/<int:user_id>", endpoint="user")


@app.route("/healthcheck")
def healthcheck():
    result = db.engine.execute("SELECT 1;").fetchone()
    return "DB: OK {}".format(result)


@app.errorhandler(404)
def handle_not_found(err):
    return jsonify({"errors": 'Resource not found'}), 404


@app.errorhandler(422)
def handle_unprocessable_entity(err):
    data = getattr(err, "data")
    if data:
        messages = data["exc"].messages
    else:
        messages = [err.args]
    return jsonify({"errors": messages}), 422


@app.errorhandler(PermissionDenied)
def handle_permission_denied(err):
    return jsonify({"errors": 'User cannot access this resource'}), 403


if __name__ == "__main__":
    app.run()

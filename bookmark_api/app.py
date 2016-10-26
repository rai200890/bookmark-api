from os.path import join, dirname
import yaml

from flask import jsonify
from flask_jwt import JWT, JWTError
from flask_principal import (
    Principal,
    Identity,
    identity_changed,
    PermissionDenied
)
from flask_swaggerui import render_swaggerui

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
        return user


def identity_loader(payload):
    user_id = payload['identity']
    try:
        user = User.query.filter_by(id=user_id).one()
        identity = Identity(user_id)
        provide_permissions(identity)
        identity_changed.send(app,
                              identity=identity)
        return user
    except Exception as e:
        app.logger.error(e)


jwt = JWT(app, authenticate, identity_loader)


principals = Principal(app)


api.add_resource(BookmarkListResource, "/bookmarks", endpoint="bookmark_list")
api.add_resource(BookmarkResource, "/bookmarks", "/bookmarks/<int:bookmark_id>", endpoint="bookmark")
api.add_resource(UserListResource, "/users", endpoint="user_list")
api.add_resource(UserResource, "/users", "/users/<int:user_id>", endpoint="user")


@app.route('/')
def root():
    return render_swaggerui(swagger_spec_path="/spec")


@app.route('/spec')
def spec():
    with open(join(dirname(__file__), 'docs/api.yml'), "r") as contents:
        docs = yaml.load(contents)
    return jsonify(docs)


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
    return jsonify({"errors": ['User cannot access this resource']}), 403


@app.errorhandler(JWTError)
def handle_invalid_credentials(err):
    return jsonify({"errors": ['Invalid credentials']}), 401


if __name__ == "__main__":
    app.run()

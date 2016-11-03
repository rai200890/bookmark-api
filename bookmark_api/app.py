from flask import jsonify
from flask_jwt import JWT, JWTError
from flask_principal import (
    Principal,
    Identity,
    identity_changed,
    PermissionDenied
)

from bookmark_api import app, db
from bookmark_api.models import User
from bookmark_api.resources.bookmark import (
    BookmarkResource,
    BookmarkListResource
)
from bookmark_api.resources.user import (
    RoleListResource,
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

bookmark_view = BookmarkResource.as_view('bookmark_resource')
bookmark_list_view = BookmarkListResource.as_view('bookmark_list_resource')
role_list_view = RoleListResource.as_view('role_list_view')
user_view = UserResource.as_view('user_resource')
user_list_view = UserListResource.as_view('user_list_resource')

app.add_url_rule('/bookmarks',
                 view_func=bookmark_list_view, methods=['GET'])
app.add_url_rule('/bookmarks', view_func=bookmark_view, methods=['POST'])
app.add_url_rule('/bookmarks/<int:bookmark_id>', view_func=bookmark_view,
                 methods=['GET', 'PUT', 'DELETE'])
app.add_url_rule('/roles',
                 view_func=role_list_view, methods=['GET'])
app.add_url_rule('/users',
                 view_func=user_list_view, methods=['GET'])
app.add_url_rule('/users', view_func=user_view, methods=['POST'])
app.add_url_rule('/users/<int:user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])


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

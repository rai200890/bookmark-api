from webargs import fields
from marshmallow import Schema
from webargs.flaskparser import use_args


class BookmarkListRequestSchema(Schema):
    per = fields.Integer(required=False)
    page = fields.Integer(required=False)

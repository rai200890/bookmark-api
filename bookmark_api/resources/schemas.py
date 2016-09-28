from marshmallow import Schema, fields


class SelfSchema(Schema):
    def get_attribute(self, attr, obj, default):
        if attr == "self":
            return obj
        return super(SelfSchema, self).get_attribute(attr, obj, default)


class PaginationSchema(Schema):
    has_next = fields.Boolean()
    has_prev = fields.Boolean()
    next_page = fields.Integer(attribute="next_num")
    prev_page = fields.Integer(attribute="prev_num")
    total = fields.Integer()
    per_page = fields.Integer()
    pages = fields.Integer()


class BookmarkListRequestSchema(Schema):
    per_page = fields.Integer(missing=15, required=False)
    page = fields.Integer(missing=1, required=False)

    class Meta:
        strict = True


class BookmarkSchema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    url = fields.Url(required=True)
    user_id = fields.Integer(required=True)


class BookmarkRequestSchema(Schema):
    bookmark = fields.Nested(BookmarkSchema)

    class Meta:
        strict = True


class BookmarkListResponseSchema(SelfSchema):
    bookmarks = fields.Nested(BookmarkSchema, many=True, attribute="items")
    pagination = fields.Nested(PaginationSchema, attribute="self")


class BookmarkResponseSchema(SelfSchema):
    bookmark = fields.Nested(BookmarkSchema, attribute="self")

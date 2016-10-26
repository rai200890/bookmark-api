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
    page = fields.Integer()


class BookmarkListRequestSchema(Schema):
    per_page = fields.Integer(missing=15, required=False)
    page = fields.Integer(missing=1, required=False)

    class Meta:
        strict = True


class BookmarkSchema(Schema):
    id = fields.Integer()
    url = fields.Url()
    title = fields.String()
    user = fields.Nested("UserSchema")
    created_at = fields.Date()


class CreateBookmarkSchema(Schema):
    id = fields.Integer()
    url = fields.Url(required=True)
    title = fields.String(required=True)


class EditBookmarkSchema(Schema):
    url = fields.Url()
    title = fields.String()


class CreateBookmarkRequestSchema(Schema):
    bookmark = fields.Nested(CreateBookmarkSchema)

    class Meta:
        strict = True


class EditBookmarkRequestSchema(Schema):
    bookmark = fields.Nested(EditBookmarkSchema)

    class Meta:
        strict = True


class BookmarkListResponseSchema(SelfSchema):
    bookmarks = fields.Nested(BookmarkSchema, many=True, attribute="items")
    pagination = fields.Nested(PaginationSchema, attribute="self")


class BookmarkResponseSchema(SelfSchema):
    bookmark = fields.Nested(BookmarkSchema, attribute="self")


class CreateUserSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer()


class EditUserSchema(Schema):
    email = fields.Email()
    password = fields.String()
    role_id = fields.Integer()


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.Email()
    role_id = fields.Integer()
    role_name = fields.String(attribute="role.name")


class CreateUserRequestSchema(Schema):
    user = fields.Nested(CreateUserSchema)

    class Meta:
        strict = True


class EditUserRequestSchema(Schema):
    user = fields.Nested(EditUserSchema)

    class Meta:
        strict = True


class UserListResponseSchema(SelfSchema):
    users = fields.Nested(UserSchema, many=True, attribute="self")


class UserResponseSchema(SelfSchema):
    user = fields.Nested(UserSchema, attribute="self")

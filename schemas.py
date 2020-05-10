from marshmallow import Schema, fields


class Tag(Schema):
    id = fields.UUID()
    label = fields.String()


class Bookmark(Schema):
    created = fields.DateTime()
    id = fields.UUID()
    label = fields.String()
    modified = fields.DateTime()
    tags = fields.List(fields.Nested(Tag))
    text = fields.String()
    url = fields.String()

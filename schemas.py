from marshmallow import Schema, fields


class Tag(Schema):
    id = fields.UUID()
    label = fields.String(required=True)


class Bookmark(Schema):
    created = fields.DateTime()
    id = fields.UUID()
    label = fields.String(required=True)
    modified = fields.DateTime()
    tags = fields.List(fields.Nested(Tag), dump_only=True)
    text = fields.String()
    url = fields.String(required=True)

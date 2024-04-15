from marshmallow import Schema, fields


class ScoreCheckerSchema(Schema):
    methods = fields.List(fields.Str(required=True))
    dataset = fields.List(fields.Raw(required=True))


class SettingsSchema(Schema):
    id = fields.Str(dump_only=True)
    openaiKey = fields.Str()

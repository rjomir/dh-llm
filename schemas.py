from marshmallow import Schema, fields


class ScoreCheckerSchema(Schema):
    methods = fields.List(fields.Str(required=True))
    dataset = fields.List(fields.Raw(required=True))


class SettingsSchema(Schema):
    id = fields.Str(dump_only=True)
    openaiKey = fields.Str(allow_none=True)
    openaiModel = fields.Str(allow_none=True)
    openaiMaxTokens = fields.Number(allow_none=True)
    bertScoreSamplingNr = fields.Number(allow_none=True)
    gEvalSamplingNr = fields.Number(allow_none=True)

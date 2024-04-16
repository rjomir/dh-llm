from db import db


class SettingsModel(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    openaiKey = db.Column(db.String(80))
    openaiModel = db.Column(db.String(80))
    openaiMaxTokens = db.Column(db.Integer)
    bertScoreSamplingNr = db.Column(db.Integer)
    gEvalSamplingNr = db.Column(db.Integer)

from db import db


class SettingsModel(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    openaiKey = db.Column(db.String(80))

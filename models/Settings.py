from db import db


class SettingsModel(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.JSON, nullable=False, default={})

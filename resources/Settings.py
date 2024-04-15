from flask.views import MethodView
from flask_smorest import Blueprint

import config
from db import db
from models import SettingsModel
from schemas import SettingsSchema

blp = Blueprint("Settings", __name__, description="Operations in settings")


@blp.route("/settings")
class Settings(MethodView):
    @blp.response(200, SettingsSchema)
    def get(self):
        return SettingsModel.query.first_or_404()

    def delete(self):
        settings = SettingsModel.query.get()

        db.session.delete(settings)
        db.session.commit()

        return {"message": "Settings deleted"}

    @blp.arguments(SettingsSchema)
    @blp.response(200, SettingsSchema)
    def post(self, settings_data):
        settings = SettingsModel(**settings_data)
        existing_settings = SettingsModel.query.first()

        try:
            if existing_settings:
                for key, value in settings_data.items():
                    setattr(existing_settings, key, value)
            else:
                db.session.add(settings)
            db.session.commit()
            return existing_settings
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

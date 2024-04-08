from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import SettingsModel
from schemas import SettingsSchema

blp = Blueprint("Settings", __name__, description="Operations in settings")

@blp.route("/settings")
class Settings(MethodView):
    @blp.response(200, SettingsSchema(many=True))
    def get(self):
        SettingsModel.query.all()

    def delete(self):
        settings = SettingsModel.query.get()

        db.session.delete(settings)
        db.session.commit()

        return {"message": "Settings deleted"}

    @blp.arguments(SettingsSchema)
    @blp.response(200, SettingsSchema)
    def post(self, settings_data):
        settings = SettingsModel(**settings_data)
        try:
            db.session.add(settings)
            db.sessioin.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred creating settings.")

        return settings

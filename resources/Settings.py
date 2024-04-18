from flask.views import MethodView
from flask_smorest import Blueprint

from db import db
from models import SettingsModel
from schemas import SettingsSchema

blp = Blueprint("Settings", __name__, description="Operations in settings")

settings_schema = SettingsSchema()


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
                existing_settings.content = settings_data['content']
            else:
                settings = SettingsModel(content=settings_data['content'])
                db.session.add(settings)
            db.session.commit()
            return settings_schema.dump(existing_settings) if existing_settings else settings_schema.dump(settings), 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

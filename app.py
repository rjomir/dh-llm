import os

from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from flask_migrate import Migrate
from resources.Settings import blp as SettingsBlueprint
from resources.Benchmark import blp as BenchmarkBlueprint
from resources.ScoreChecker import blp as ScoreCheckerBluePrint
from db import db
import config


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Detect LLM Hallucinations"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)
    api = Api(app)
    config.init()

    api.register_blueprint(SettingsBlueprint)
    api.register_blueprint(BenchmarkBlueprint)
    api.register_blueprint(ScoreCheckerBluePrint)

    CORS(app, origins='*')

    return app

from flask.views import MethodView
from flask_smorest import Blueprint

from services.parsers.DollyParser import DollyParser
from services.parsers.DropParser import DropParser
from services.parsers.CovidParser import CovidParser

blp = Blueprint("Benchmarks", __name__, description="Operations in benchmarks")


@blp.route("/benchmark/<string:benchmark_id>")
class Benchmark(MethodView):
    @blp.response(200)
    def get(self, benchmark_id):
        if benchmark_id == 'databricks-dolly':
            return DollyParser().display()
        if benchmark_id == 'drop':
            return DropParser().display()
        if benchmark_id == 'covid-qa':
            return CovidParser().display()
        return '', 204

import concurrent.futures

from flask.views import MethodView
from flask_smorest import Blueprint
from services.scorecheckers import ngram, bert

from schemas import ScoreCheckerSchema

blp = Blueprint("ScoreChecker", __name__, description="Operations in score checker")


@blp.route("/score")
class ScoreChecker(MethodView):

    @blp.arguments(ScoreCheckerSchema)
    @blp.response(200)
    def post(self, request_data):
        methods = request_data['methods']
        dataset = request_data['dataset']

        results = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for method in methods:
                checker = None
                if method == 'ngram':
                    checker = ngram.SelfCheckNgram(1, True, dataset)
                elif method == 'bert':
                    checker = bert.SelfCheckBert(dataset)
                future = executor.submit(checker.evaluate)
                futures.append((method, future))

            for method, future in futures:
                result = future.result()
                results[method] = result

        return results

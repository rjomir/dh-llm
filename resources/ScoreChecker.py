import concurrent.futures

from flask.views import MethodView
from flask_smorest import Blueprint
from lib.scorers import selfcheck_bert, selfcheck_ngram, chain_poll, g_eval, ref_checker

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
                    checker = selfcheck_ngram.SelfCheckNgram(1, True, dataset)
                elif method == 'bert':
                    checker = selfcheck_bert.SelfCheckBert(dataset)
                elif method == 'chainpoll':
                    checker = chain_poll.ChainPoll(dataset)
                elif method == 'g-eval':
                    checker = g_eval.GEval(dataset)
                elif method == 'ref-checker':
                    checker = ref_checker.RefChecker(dataset)
                future = executor.submit(checker.evaluate)
                futures.append((method, future))

            for method, future in futures:
                result = future.result()
                results[method] = result

        return results

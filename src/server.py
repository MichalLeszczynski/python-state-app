import json
import flask

from health_checker import HealthChecker


app = flask.Flask(__name__)
app.config["DEBUG"] = True

health_checker = HealthChecker()


@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
@app.route("/<path:anypath>/health", methods=["GET"])
def health(anypath=None):
    return health_checker.dump_info()


@app.route("/api/echo", methods=["GET"])
def api():
    data_dict = dict(flask.request.args.items())
    return json.dumps(data_dict)


app.run(host="0.0.0.0", port=80)

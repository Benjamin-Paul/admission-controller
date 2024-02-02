import http
import logging
# import base64
# import copy
# import json
# import random

from flask import Flask, jsonify, request
# import jsonpatch

app = Flask(__name__)


@app.route("/validate", methods=["POST"])
def validate():
    app.logger.info('Validation request received')

    allowed = True
    message = ""
    try:
        if "kubernetes.io/change-cause" not in request.json["request"]["object"]["metadata"]["annotations"]:
            allowed = False
            message = "kubernetes.io/change-cause is mandatory for deployments in this namespace. See documentation for more information."
        elif request.json["request"]["oldObject"] is None:
            message = "Ok. First change-cause provided."
        elif request.json["request"]["oldObject"]["metadata"]["annotations"]["kubernetes.io/change-cause"] == request.json["request"]["object"]["metadata"]["annotations"]["kubernetes.io/change-cause"]:
            allowed = False
            message = "kubernetes.io/change-cause unchanged. You must modify it."
    except KeyError:
        allowed = False
        message = "Inernal error. Reach out to the developper : https://github.com/Benjamin-Paul"

    app.logger.info('Validation request processed')

    return jsonify(
        {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "allowed": allowed,
                "uid": request.json["request"]["uid"],
                "status": {"message": message},
            }
        }
    )

# Mutating admission controller example
'''
@app.route("/mutate", methods=["POST"])
def mutate():
    spec = request.json["request"]["object"]
    modified_spec = copy.deepcopy(spec)

    try:
        modified_spec["metadata"]["labels"]["example.com/new-label"] = str(
            random.randint(1, 1000)
        )
    except KeyError:
        pass
    patch = jsonpatch.JsonPatch.from_diff(spec, modified_spec)
    return jsonify(
        {
            "response": {
                "allowed": True,
                "uid": request.json["request"]["uid"],
                "patch": base64.b64encode(str(patch).encode()).decode(),
                "patchtype": "JSONPatch",
            }
        }
    )
'''

@app.route("/health", methods=["GET"])
def health():
    return ("", http.HTTPStatus.NO_CONTENT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=443, ssl_context=("ssl/tls.crt", "ssl/tls.key"))

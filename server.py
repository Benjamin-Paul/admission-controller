import base64
import copy
import http
import json
import random

import jsonpatch
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/validate", methods=["POST"])
def validate():
    allowed = True
    try:
        if "kubernetes.io/change-cause" not in request.json["request"]["object"]["metadata"]["annotations"]:
            allowed = False
            return jsonify(
                {
                    "apiVersion": "admission.k8s.io/v1",
                    "kind": "AdmissionReview",
                    "response": {
                        "allowed": allowed,
                        "uid": request.json["request"]["uid"],
                        "status": {"message": "kubernetes.io/change-cause is mandatory for deployments in this namespace."},
                    }
                }
        elif request.json["request"]["object"]["metadata"]["annotations"]["kubectl.kubernetes.io/last-applied-configuration"]["metadata"]["annotations"]["kubernetes.io/change-cause"] == request.json["request"]["object"]["metadata"]["annotations"]["kubernetes.io/change-cause"]:
            allowed = False
            return jsonify(
                {
                    "apiVersion": "admission.k8s.io/v1",
                    "kind": "AdmissionReview",
                    "response": {
                        "allowed": allowed,
                        "uid": request.json["request"]["uid"],
                        "status": {"message": "kubernetes.io/change-cause unchanged. You must modify it."}
                    }
                }
    except KeyError:
        pass
    return jsonify(
        {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "allowed": allowed,
                "uid": request.json["request"]["uid"],
                "status": {"message": "container images are prohibited. That sucks, eh ?"},
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
    app.run(host="0.0.0.0", port=443, ssl_context=("ssl/tls.crt", "ssl/tls.key"))

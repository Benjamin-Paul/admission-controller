from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def handle_admission(request):
    response = {
        "allowed": False,
        "status": {
            "reason": "ChangeCauseNotModified",
            "message": "The kubernetes.io/change-cause field must be modified.",
        },
    }
    return response

@app.route("/test", methods=["GET"])
def test():
    return "Yo this a test"

@app.route("/", methods=["POST"])
def admission_handler():
    try:
        admission_review = request.json
        admission_review["response"] = handle_admission(admission_review["request"])
        return jsonify(admission_review)
    except Exception as err:
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, ssl_context=("ssl/tls.crt", "ssl/tls.key"))

from app.views import app
from flask import redirect, jsonify, request

@app.route("/")
def main():
    return redirect("apidocs/")

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"msg":"Bad reqeust"}), 400

@app.errorhandler(401)
def not_authorized(error):
    return jsonify({"msg":"Not authorized."}), 401

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"msg":"Route does not exist"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"msg":"Method not allowed"}), 405

@app.before_request
def check_for_json():
    if not request.content_type == 'application/json':
        if not request.method == 'GET' \
                and '/v1/' in request.path:
            return jsonify({"msg": "Content type not json"})

if __name__ == '__main__':
    app.run(debug=True)

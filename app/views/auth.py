from app.models.user import User
import re

from flasgger import swag_from
from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from werkzeug.security import check_password_hash, generate_password_hash

from app.views import app
from app.views import db_conn, empty_field
from app.models.question import Question

@app.route('/v1/auth/signup', methods=['POST'])
@swag_from('docs/register.yml')
def add_user():
    """add user adds a user having validated the inputs."""
    if not isinstance(request.json.get('email'), str):
        return jsonify({"msg":"Email must be a string. Example: john@exam.com"}), 400

    email = request.json.get('email').strip()
    if not email:
        return jsonify({"msg":"Email field is empty."}), 400

    if not isinstance(request.json.get('name'), str):
        return jsonify({"msg":"Name must be a string. Example: johndoe"}), 400
        
    name = request.json.get('name').strip()
    if not name:
        return jsonify({"msg":"Name field is empty"}), 400
    password = str(request.json.get('password')).strip()

    if  email and name and password:
        if not re.match(r'^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return jsonify({"msg":"Invalid email. Example: john@exam.com"}), 400

        if len(name) > 15:
            return jsonify({"msg": "Name is too long, max 15"}), 400

        if not re.match(r'^[a-z0-9_]+$', name):
            return jsonify({"msg": "Name can only contain lowercase a-z, 0-9 and _"}), 400

        if len(password) < 8:
            return jsonify({"msg":"Password too short, min 8 chars"}), 400

        if len(password) > 12:
            return jsonify({"msg": "Password too long, max 12"}), 400

        new_user = User(email, name, generate_password_hash(password))
        return new_user.insert_new_record()

    output = empty_field
    return jsonify(output), 400


@app.route('/v1/auth/signin', methods=['POST'])
@swag_from('docs/sigin.yml')
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    if not isinstance(request.json.get('email'), str):
        return jsonify({"msg":"Email must be a string. Example: john@exam.com"}), 400
        
    email = request.json.get('email').strip()
    password = str(request.json.get('password')).strip()

    if not email:
        return jsonify(empty_field), 400
    if not password:
        return jsonify(empty_field), 400

    output = ""
    items = db_conn.query_single(email) 
    output = output + str(items)
    hashed_password = db_conn.return_password(email)

    if email in output:
        if check_password_hash(hashed_password[0], password):
            user_id = db_conn.return_id(email)
            access_token = create_access_token(identity=user_id[0])
            output = {'message':'Successful login'}
            access_token_output = {'access_token':"%s" % (access_token)}
            return jsonify(output, access_token_output), 200

    output = {"msg": "Bad username or password"}
    resp = jsonify(output)
    resp.status_code = 200
    return resp

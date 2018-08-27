from flask import Flask
from flask import Flask, request, jsonify
# local import
from instance.config import app_config
import json

def create_app(config_name):
    from app.models.user import User
    from app.database import Database
    from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity    
    )

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

  
    jwt = JWTManager(app)

    db_conn = Database()
    empty_field = {'message': 'A field is empty'}
    
    @app.route('/auth/signup', methods=['POST'])
    def add_user():
        """add user adds a user"""
        if request.json.get('email') and request.json.get('name') and request.json.get('password'):
            new_user = User(request.json.get('email'), request.json.get('name'), request.json.get('password'))
            output = new_user.insert_new_record()
            return jsonify(output), 201

        output = empty_field
        return jsonify(output), 400

    @app.route('/auth/signin', methods=['POST'])
    def login():
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        email = request.json.get('email')
        password = request.json.get('password')

        if not email:
            return jsonify({"msg": "Missing username parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400
    
        output = ""
        db_conn = Database()
        items = db_conn.query_single(email) 
        output = output + str(items)
    
        if email in output and password in output:
            # Identity can be any data that is json serializable
            user_id = db_conn.return_id(email)
            access_token = create_access_token(identity=user_id[0])
            return jsonify(access_token=access_token), 200
    
        output = {"msg": "Bad username or password"}
        resp = jsonify(output)
        resp.status_code = 200
        return resp

    return app

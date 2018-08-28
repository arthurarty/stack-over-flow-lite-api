from flask import Flask
from flask import Flask, request, jsonify
# local import
from app.config import app_config
import json

def create_app():
    from app.models.user import User
    from app.database import Database
    from app.models.question import Question
    from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity    
    )

    app = Flask(__name__, instance_relative_config=True)
  
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
            output = {'message':'Successful login'}
            access_token_output = {'access_token':"%s" % (access_token)}
            return jsonify(output, access_token_output), 200
    
        output = {"msg": "Bad username or password"}
        resp = jsonify(output)
        resp.status_code = 200
        return resp

    @app.route('/v1/questions', methods=['POST'])
    @jwt_required
    def add_question():
        current_user = get_jwt_identity()
        if request.form['title']:
            new_question = Question(int(current_user[0]), request.form['title'])
            return new_question.insert_new_record()
        
        output = empty_field
        return jsonify(output), 400

    @app.route('/v1/questions', methods=['GET'])
    @jwt_required
    def fetch_all_questions():
        output = db_conn.query_all("questions")
        return jsonify(output), 200
    
    @app.route('/v1/questions/<int:question_id>/')
    @jwt_required
    def fetch_single_question(question_id):
        """fetch_single_questions method returns single question with input being of the type int. 
        """
        output = db_conn.query_single_row("questions", "question_id", question_id)
        if not output:
            output = {
                'message': 'Question Not Found: ' + request.url,
            }
            return jsonify(output), 404

        return jsonify(output), 200
    return app

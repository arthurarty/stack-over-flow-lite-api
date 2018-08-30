import re

from flasgger import swag_from
from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from werkzeug.security import check_password_hash, generate_password_hash

from app import create_app
from app.database import Database
from app.models.answer import Answer
from app.models.question import Question
from app.models.user import User

app = create_app()

db_conn = Database()
empty_field = {'msg': 'A field is empty'}

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
        output = new_user.insert_new_record()
        return jsonify({"msg":"User account successfully created."}), 201

    output = empty_field
    return jsonify(output), 400

@app.route('/v1/auth/signin', methods=['POST'])
@swag_from('docs/sigin.yml')
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email').strip()
    password = str(request.json.get('password')).strip()

    if not email:
        return jsonify(empty_field), 400
    if not password:
        return jsonify(empty_field), 400

    output = ""
    db_conn = Database()
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

@app.route('/v1/questions', methods=['POST'])
@jwt_required
@swag_from('docs/post_question.yml')
def add_question():
    """method to add question to database"""
    current_user = get_jwt_identity()
    title = str(request.json.get('title')).strip()

    if not title:
        return jsonify({"msg":"Title field is empty"}), 400

    if request.json.get('title'):
        new_question = Question(int(current_user), request.json.get('title'))
        return new_question.insert_new_record()
        
    else:
        output = empty_field
        return jsonify(output), 400

@app.route('/v1/questions', methods=['GET'])
@jwt_required
@swag_from('docs/get_questions.yml')
def fetch_all_questions():
    """method fetchs all questions from the database"""
    output = db_conn.query_all("questions")
    return jsonify(output), 200

@app.route('/v1/questions/<int:question_id>/', methods=['GET'])
@jwt_required
@swag_from('docs/get_single_question.yml')
def fetch_single_question(question_id):
    """fetch_single_questions method returns single question with input being of the type int. 
    """
    output = db_conn.query_single_row("questions", "question_id", question_id)
    if not output:
        output = {
            'message': 'Question Not Found: ' + request.url,
        }
        return jsonify(output), 404
    answers = db_conn.query_all_where_id("answers", "question_id", question_id)
    return jsonify(output, {"answers": answers}), 200

@app.route('/v1/questions/<int:question_id>/delete', methods=['DELETE'])
@jwt_required
@swag_from('docs/delete_question.yml')
def delete_question(question_id):
    """delete question and corresponding answers 
    """
    output = db_conn.return_user_id("questions", "question_id", question_id)
    if not output:
        output = {
            'message': 'Question Not Found: ' + request.url,
        }
        return jsonify(output), 404
    current_user = get_jwt_identity()
    if current_user[0] in output:
        db_conn.delete_question(question_id)
        return jsonify({'message':'Question Deleted'}), 200
    return jsonify({'message':'No rights to delete question'}), 401

@app.route('/v1/questions/<int:question_id>/answers', methods=['POST'])
@jwt_required
@swag_from('docs/add_answer.yml')
def add_answer_to_question(question_id):
    """method to add answer to question"""
    title = str(request.json.get('title')).strip()
    if title:
        output = db_conn.return_user_id("questions", "question_id", question_id)
        if not output:
            output = {
                'message': 'Question Not Found: ' + request.url,
            }
            return jsonify(output), 404
        current_user = get_jwt_identity()
        new_answer = Answer(question_id, request.json.get('title'), current_user)
        new_answer.insert_new_record()
        return jsonify({"msg": "Answer added to question"}), 201

    output = empty_field
    return jsonify(output), 400

@app.route('/v1/questions/<int:question_id>/answers/<int:answer_id>/mark', methods=['PUT'])
@jwt_required
@swag_from('docs/mark_answer_preferred.yml')
def mark_answer_preferred(question_id, answer_id):
    """method to mark answer as preferred"""
    output = db_conn.return_user_id("questions", "question_id", question_id)
    if not output:
        output = {
            'message': 'Question Not Found: ' + request.url,
        }
        return jsonify(output), 404
    current_user = get_jwt_identity()
    if current_user[0] in output:
        value = "True"
        db_conn.update_record("answers", "preferred", value, "answer_id", answer_id)
        return jsonify({'msg':'Answer marked as preferred'}), 201
    return jsonify({'msg':'Not authorized to mark as preferred'}), 401

@app.route('/v1/questions/<int:question_id>/answers/<int:answer_id>/edit', methods=['PUT'])
@jwt_required
@swag_from('docs/put_answer.yml')
def edit_answer(question_id,answer_id):
    title = str(request.json.get('title')).strip()
    if  title:
        """method to mark answer as preferred"""
        output = db_conn.return_user_id("answers", "answer_id", answer_id)
        if not output:
            output = {
                'message': 'Question Not Found: ' + request.url,
         }
            return jsonify(output), 404
        current_user = get_jwt_identity()
        if current_user[0] in output:
            db_conn.update_record("answers", "title", request.json.get('title'), "answer_id", answer_id)
            return jsonify({'msg':'Answer successfully edited'}), 201
        return jsonify({"msg":"No rights to edit answer"}), 401
    return jsonify(empty_field), 400

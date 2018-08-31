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


@app.route('/v1/questions', methods=['POST'])
@jwt_required
@swag_from('docs/post_question.yml')
def add_question():
    """method to add question to database"""
    current_user = get_jwt_identity()
    title = str(request.json.get('title')).strip()

    if not title:
        return jsonify({"msg": "Title field is empty"}), 400

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
        return jsonify({'message': 'Question Not Found:'}), 404
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
        return jsonify({'message': 'Question Not Found:'}), 404
    current_user = get_jwt_identity()
    if current_user in output:
        db_conn.delete_question(question_id)
        return jsonify({'message': 'Question Deleted'}), 200
    return jsonify({'message': 'No rights to delete question'}), 401

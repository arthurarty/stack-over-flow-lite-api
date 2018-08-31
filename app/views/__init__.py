import re

from flasgger import swag_from
from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from werkzeug.security import check_password_hash, generate_password_hash

from app import create_app
from app.database import Database
from app.models.answer import Answer

app = create_app()
db_conn = Database()
empty_field = {'msg': 'A field is empty'}

#import auth views
from app.views import auth

#import question views. 
from app.views import questions

@app.route('/v1/questions/<int:question_id>/answers', methods=['POST'])
@jwt_required
@swag_from('docs/add_answer.yml')
def add_answer_to_question(question_id):
    """method to add answer to question"""
    title = str(request.json.get('title')).strip()
    if title:
        output = db_conn.return_user_id("questions", "question_id", question_id)
        if not output:
            return jsonify({'message': 'Question Not Found:'}), 404
        
        current_user = get_jwt_identity()
        new_answer = Answer(question_id, request.json.get('title'), current_user)
        new_answer.insert_new_record()
        return jsonify({"msg": "Answer added to question" + request.url,}), 201

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
    if current_user in output:
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
        if current_user in output:
            db_conn.update_record("answers", "title", request.json.get('title'), "answer_id", answer_id)
            return jsonify({'msg':'Answer successfully edited'}), 201
        return jsonify({"msg":"No rights to edit answer"}), 401
    return jsonify(empty_field), 400

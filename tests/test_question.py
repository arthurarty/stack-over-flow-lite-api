from app.models.question import Question
import pytest
from tests import (client, post_json, post_json_header,
 signin, user_two, put_json_header)

def test_is_instance_of_question():
    new_question = Question(5, "Hello there")
    assert isinstance(new_question, Question)

def test_add_question(client):
    resp = post_json_header(client, '/v1/questions', {
        "title": "big is big",}, 
    headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 201

def test_get_questiosn(client):
    resp = client.get('/v1/questions', headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 200

def test_get_single_question(client):
    resp = client.get('/v1/questions/1', headers={'Authorization': 'Bearer ' + signin(client)})
    assert b'title' in resp.data

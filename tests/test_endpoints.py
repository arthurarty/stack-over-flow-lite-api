import pytest
from tests import (client, post_json, post_json_header,
 signin, user_two, put_json_header)

def test_user_creation(client):
    resp = post_json(client, '/v1/auth/signup', { 
	"email": "test@test.com",
    "name": "test",
	"password":"testAs1v"})
    assert b'User successfully created' in resp.data
    assert resp.status_code == 201

def test_duplicate_user_creation(client):
    resp = post_json(client, '/v1/auth/signup', { 
	"email": "test@test.com",
    "name": "test",
	"password":"testAs1v"})
    assert b'Email address already exists' in resp.data
    assert resp.status_code == 400

def test_user_login(client):
    resp = post_json(client, '/v1/auth/signin', { 
	"email": "test@test.com",
	"password":"testAs1v"})
    assert b'Successful login' in resp.data
    assert resp.status_code == 200

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

def test_post_answer(client):
    resp = post_json_header(client,'/v1/questions/1/answers', {
        "title": "how to do it."
    },
    headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 201

def test_mark_preferred_answer(client):
    resp = client.put('/v1/questions/1/answers/1/mark', headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 201
    assert b'Answer marked as preferred' in resp.data

def test_edit_answer(client):
    resp = put_json_header(client,'/v1/questions/1/answers/1/edit', {
        "title": "this is actually not how its done."
    },
    headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 201
    assert b'Answer successfully edited' in resp.data

def test_edit_answer_wrong_user(client):
    resp = put_json_header(client,'/v1/questions/1/answers/1/edit', {
        "title": "this is actually not how its done."
    },
    headers={'Authorization': 'Bearer ' + user_two(client)})
    assert resp.status_code == 401
    assert b'No rights to edit answer' in resp.data

def test_delete_question_by_another_user(client):
    resp = client.delete('/v1/questions/1/delete', headers={'Authorization': 'Bearer ' + user_two(client)})
    assert resp.status_code == 401
    assert b'No rights to delete question' in resp.data


def test_delete_question(client):
    resp = client.delete('/v1/questions/1/delete', headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 200
    assert b'Question Deleted' in resp.data

 
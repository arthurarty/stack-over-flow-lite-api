import http.client
import pytest
from app.views import app
import psycopg2
import json

@pytest.fixture
def client():
    client = app.test_client()
    yield client

def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')

def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))

def signin(client):
    resp = post_json(client, '/auth/signin', { 
	"email": "test@test.com",
	"password":"test"})
    access = json_of_response(resp)
    access_token = access[1]['access_token']
    return access_token

def user_two(client):
    resp = post_json(client, '/auth/signup', { 
	"email": "user@test.com",
    "name": "user",
	"password":"user"})
    resp = post_json(client, '/auth/signin', { 
	"email": "user@test.com",
	"password":"user"})
    access = json_of_response(resp)
    access_token = access[1]['access_token']
    return access_token

def test_user_creation(client):
    resp = post_json(client, '/auth/signup', { 
	"email": "test@test.com",
    "name": "test",
	"password":"test"})
    assert b'User account successfully created' in resp.data
    assert resp.status_code == 201

def test_user_login(client):
    resp = post_json(client, '/auth/signin', { 
	"email": "test@test.com",
	"password":"test"})
    assert b'Successful login' in resp.data
    assert resp.status_code == 200

def test_add_question(client):
    resp = client.post('/v1/questions', headers={'Authorization': 'Bearer ' + signin(client)}, 
    data=dict( title= "big man",))
    assert resp.status_code == 201

def test_get_questiosn(client):
    resp = client.get('/v1/questions', headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 200

def test_get_single_question(client):
    resp = client.get('/v1/questions/1', headers={'Authorization': 'Bearer ' + signin(client)})
    assert b'title' in resp.data

def test_post_answer(client):
    resp = client.post('/v1/questions/1/answers', headers={'Authorization': 'Bearer ' + signin(client)}, 
    data=dict( title= "how to do this thing",))
    assert resp.status_code == 201

def test_delete_question_by_another_user(client):
    resp = client.delete('/v1/questions/1/delete', headers={'Authorization': 'Bearer ' + user_two(client)})
    assert resp.status_code == 401
    assert b'No rights to delete question' in resp.data

def test_delete_question(client):
    resp = client.delete('/v1/questions/1/delete', headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 200
    assert b'Question Deleted' in resp.data
 
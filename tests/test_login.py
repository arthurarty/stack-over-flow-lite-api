import http.client
import pytest
from app import create_app
import psycopg2
import json

@pytest.fixture
def client():
    app = create_app(config_name="testing")
    client = app.test_client()
    yield client

def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')

def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))

def test_user_creation(client):
    resp = post_json(client, '/auth/signup', { 
	"email": "test@test.com",
    "name": "test",
	"password":"test"})
    assert b'test@test.com' in resp.data
    assert resp.status_code == 201

def test_user_login(client):
    resp = post_json(client, '/auth/signin', { 
	"email": "test@test.com",
	"password":"test"})
    assert b'Successful login' in resp.data
    assert resp.status_code == 200


def test_add_question(client):
    resp = post_json(client, '/auth/signin', { 
	"email": "test@test.com",
	"password":"test"})
    access = json_of_response(resp)
    access_token = access[1]['access_token']
    resp = client.post('/v1/questions', headers={'Authorization': 'Bearer ' + access_token}, 
    data=dict( title= "big man",))
    assert resp.status_code == 201

def test_get_questiosn(client):
    resp = post_json(client, '/auth/signin', { 
	"email": "test@test.com",
	"password":"test"})
    access = json_of_response(resp)
    access_token = access[1]['access_token']
    resp = client.get('/v1/questions', headers={'Authorization': 'Bearer ' + access_token})
    assert resp.status_code == 200

def test_get_single_question(client):
    resp = post_json(client, '/auth/signin', { 
	"email": "test@test.com",
	"password":"test"})
    access = json_of_response(resp)
    access_token = access[1]['access_token']
    resp = client.get('/v1/questions/1', headers={'Authorization': 'Bearer ' + access_token})
    assert b'title' in resp.data
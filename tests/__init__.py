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

def post_json_header(client, url, json_dict, headers):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json', headers=headers)

def put_json_header(client, url, json_dict, headers):
    """Send dictionary json_dict as a json to the specified url """
    return client.put(url, data=json.dumps(json_dict), content_type='application/json', headers=headers)

def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))

def signin(client):
    resp = post_json(client, '/v1/auth/signin', { 
	"email": "test@test.com",
	"password":"testAs1v"})
    access = json_of_response(resp)
    access_token = access[1]['access_token']
    return access_token

def user_two(client):
    resp = post_json(client, '/v1/auth/signup', { 
	"email": "user@test.com",
    "name": "user",
	"password":"userIs4a"})
    resp = post_json(client, '/v1/auth/signin', { 
	"email": "user@test.com",
	"password":"userIs4a"})
    access = json_of_response(resp)
    access_token = access[1]['access_token']
    return access_token

def create_question(client):
    resp = post_json_header(client, '/v1/questions', {
        "title": "question_2",}, 
    headers={'Authorization': 'Bearer ' + signin(client)})
    
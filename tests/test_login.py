import http.client
import pytest
from app import create_app
import psycopg2
import json
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity    
    )

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


    
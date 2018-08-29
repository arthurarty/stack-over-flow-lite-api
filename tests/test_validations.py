import pytest
import json
from app.views import app
from test_endpoints import post_json

@pytest.fixture
def client():
    client = app.test_client()
    yield client

def test_long_name(client):
    resp = post_json(client, '/auth/signup', { 
	"email": "test@test.com",
    "name": "testismeyoutoo",
	"password":"testsfas"})
    assert b'Name too long' in resp.data
    assert resp.status_code == 400


def test_invalid_name(client):
    resp = post_json(client, '/auth/signup', { 
	"email": "test@test.com",
    "name": "testAsBA",
	"password":"testsfas"})
    assert b'Name can only contain lowercase a-z, 0-9 and _' in resp.data
    assert resp.status_code == 400

def test_short_password(client):
    resp = post_json(client, '/auth/signup', { 
	"email": "test@test.com",
    "name": "test",
	"password":"test"})
    assert b'Password too short' in resp.data
    assert resp.status_code == 400

def test_long_password(client):
    resp = post_json(client, '/auth/signup', { 
	"email": "test@test.com",
    "name": "test",
	"password":"testsfsfdsfsdf"})
    assert b'Password too long' in resp.data
    assert resp.status_code == 400

def test_invalid_email(client):
    resp = post_json(client, '/auth/signup', { 
	"email": "testtest",
    "name": "test",
	"password":"testsfsfdsfsdf"})
    assert b'Invalid email' in resp.data
    assert resp.status_code == 400

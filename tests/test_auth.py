import pytest
from tests import (client, post_json, post_json_header,
 signin, user_two, put_json_header)
from app.models.user import User

def test_is_instance_of_user():
    new_user = User("arthur.nangai@gmail.com", "Arthur Nangai", "Nangai")
    assert isinstance(new_user, User)

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
 
import pytest
import json
from app.views import app
from test_endpoints import (
    client, post_json, post_json_header,
    put_json_header, signin
)

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

def test_empty_post_title_question(client):
    resp = post_json_header(client, '/v1/questions', {
        "title": " ",}, 
    headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 400
    assert b'A field is empty' in resp.data

def test_empty_post_title_answer(client):
    resp = post_json_header(client,'/v1/questions/1/answers', {
        "title": " "
    },
    headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 400
    assert b'A field is empty' in resp.data

def test_empty_post_title_edit_answer(client):  
    resp = put_json_header(client,'/v1/questions/1/answers/1/edit', {
        "title": " "
    },
    headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 400
    assert b'A field is empty' in resp.data

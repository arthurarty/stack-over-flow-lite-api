from app.models.answer import Answer
from tests import (client, post_json, post_json_header,
                   signin, user_two, put_json_header)
import pytest


def test_is_instance_of_answer():
    new_answer = Answer(5, "Hello there", "Nangai")
    assert isinstance(new_answer, Answer)


def test_post_answer(client):
    resp = post_json_header(client, '/v1/questions/1/answers', {
        "title": "how to do it."
    },
        headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 201


def test_mark_preferred_answer(client):
    resp = client.put('/v1/questions/1/answers/1/mark',
                      headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 201
    assert b'Answer marked as preferred' in resp.data


def test_edit_answer(client):
    resp = put_json_header(client, '/v1/questions/1/answers/1/edit', {
        "title": "this is actually not how its done."
    },
        headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 201
    assert b'Answer successfully edited' in resp.data


def test_edit_answer_wrong_user(client):
    resp = put_json_header(client, '/v1/questions/1/answers/1/edit', {
        "title": "this is actually not how its done."
    },
        headers={'Authorization': 'Bearer ' + user_two(client)})
    assert resp.status_code == 401
    assert b'No rights to edit answer' in resp.data


def test_delete_question_by_another_user(client):
    resp = client.delete('/v1/questions/1/delete',
                         headers={'Authorization': 'Bearer ' + user_two(client)})
    assert resp.status_code == 401
    assert b'No rights to delete question' in resp.data


def test_delete_question(client):
    resp = client.delete('/v1/questions/1/delete',
                         headers={'Authorization': 'Bearer ' + signin(client)})
    assert resp.status_code == 200
    assert b'Question Deleted' in resp.data

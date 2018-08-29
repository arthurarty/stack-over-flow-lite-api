"""tests fro the user class"""
from app.models.user import User
import pytest

def test_is_instance_of_user():
    new_user = User("arthur.nangai@gmail.com", "Arthur Nangai", "Nangai")
    assert isinstance(new_user, User)
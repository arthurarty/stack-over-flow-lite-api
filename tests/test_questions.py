from app.models.question import Question
import pytest

#each question must be an instance of the question class
def test_is_instance_of_question():
    new_question = Question(5, "Hello there")
    assert isinstance(new_question, Question)

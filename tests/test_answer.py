from app.models.answer import Answer

#each question must be an instance of the question class
def test_is_instance_of_answer():
    new_answer = Answer(5, "Hello there", "Nangai")
    assert isinstance(new_answer, Answer)

    
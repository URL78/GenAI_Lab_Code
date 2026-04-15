import pytest
from GenAI_lab_8 import InterviewEvaluator

def test_emptyanswer():
    evaluate=InterviewEvaluator()
    with pytest.raises(ValueError, match="Answers cannot be empty"):
        evaluate.evaluate([])

def test_short_answer():
    evaluate=InterviewEvaluator()
    answers=["url"]
    assert evaluate.evaluate(answers)==5

def test_large_answer():
    evaluate=InterviewEvaluator()
    answers=["d he gcc ejc  hjc bc cc hich cdeg ed dcb cchc cccbc c ccgc ccchc xd xdg chl   cef cchld de  delc cdg dy uxgdel xdh xdegxdex"]
    assert evaluate.evaluate(answers)==10

def test_medium_answer():
    evaluate=InterviewEvaluator()
    answers=["dhegcc ejchjc bc cchich cdeged dcb cchc"]
    assert evaluate.evaluate(answers)==7 

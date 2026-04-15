import pytest
from GenAI_lab_8 import MCQGenerator

noskill=MCQGenerator([])
languageskill=MCQGenerator(["python"])
easyskill=MCQGenerator(["sql"],"easy")
mediumskill=MCQGenerator(["machine learning"] ,"medium")
hardskill=MCQGenerator(["java"] ,"hard")

def test_noskill_error():
    with pytest.raises(ValueError, match="No skills provided"):
        noskill.generate_question()

def test_languageskill():
    assert languageskill.generate_question()=="What is python?"

def test_easyskill():
    assert easyskill.generate_question()=="What is sql?"

def test_mediumskill():
    assert mediumskill.generate_question()=="Explain key concepts of machine learning?"

def test_hardskill():
    assert hardskill.generate_question()=="Design a system using nlp"

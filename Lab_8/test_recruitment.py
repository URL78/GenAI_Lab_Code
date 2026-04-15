import pytest
import re
from GenAI_lab_8 import RecruitmentSystem

resume6= "education: Mtech , experience: 15 years , skills : OS, CN, sql"
resume7= "education: Btech , experience: -4 years , skills : sql"
resume8= "education: PHD , experience: 4 years , skills : AI, ML, NLP, DL, OS, CN, DBMS, COA"

def test_sys1():
    op=RecruitmentSystem(resume7,'easy')
    result=op.process()
    assert 'skills' in result
    assert 'experience' in result
    assert 'score' in result
    assert 'question' in result
    assert result['experience']==0
    assert len(result['skills'])>1

def test_sys2():
    op=RecruitmentSystem(resume8,'medium')
    result = op.process()
    assert result['experience']==4
    assert len(result['skills'])==1
    assert result['score']>10

import pytest
from GenAI_lab_8 import ResumeParser

resume1= "education: Mtech , experience: 3 years , skills : Distributed systems, Deep Learning, AI, NLP,OS, CN"
resume2= "education: Mtech , experience: 4 years , skills : python, Distributed database, machine learning, AI, NLP,OS, CN"
resume3= "education: Btech , experience: 1 years , skills : python, java, sql, AI, nlp, OS, CN"
resume4= "education: Btech , experience: 6 years , skills :  "
resume5= "education: Btech , experience: 0 years , skills : c++"
resume6= "education: Mtech , experience: 15 years , skills : OS, CN, sql"
resume7= "education: Btech , experience: -4 years , skills : sql"
resume8= "education: PHD , experience: 4 years , skills : AI, ML, NLP, DL, OS, CN, DBMS, COA"

def test_skill():
    rp=ResumeParser(resume7)
    assert rp.extract_skills()==["sql"]
    
def test_exp():
    rp=ResumeParser(resume7)
    assert rp.extract_experience()==0


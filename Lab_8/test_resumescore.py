import pytest
from GenAI_lab_8 import CandidateScorer

def test_noexp():
    score=CandidateScorer([], 0)
    assert score.calculate_score()==10

def test_lessexp():
    score=CandidateScorer(["Python","SQL"],1)
    assert score.calculate_score()==30

def test_highexp():
    score=CandidateScorer(["Python","SQL","ML","DL"],6)
    assert score.calculate_score()==70

def test_mediumexp():
    score=CandidateScorer(["Python","SQL","ML"],4)
    assert score.calculate_score()==50


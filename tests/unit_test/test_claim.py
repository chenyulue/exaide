import pytest
import exaide.model as m

@pytest.fixture
def claim_model(claim):
    return m.ClaimModel(claim)

def test_claims_has_content(claim_model, claim):
    assert claim_model._claim == claim
    assert claim_model._sensitive_words == []

def test_split_claims(claim_model):
    claim_items = claim_model.split_claims()
    assert len(claim_items) == 8
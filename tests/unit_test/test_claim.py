import pytest
import exaide.model as m

@pytest.fixture
def claim_model(claim):
    return m.ClaimModel(claim)

def test_claims_has_content(claim_model, claim):
    assert claim_model._claims == claim
    assert claim_model._sensitive_words == []
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
    assert claim_items[1] == m.Claim(
        2,
        "根据权利要求1所述的MOS晶体管电路",
        [
            "2.根据权利要求1所述的MOS晶体管电路，其特征在于：所述电阻器元件为上拉电阻或下拉电阻。"
        ],
    )
    assert claim_items[0] == m.Claim(
        1,
        "一种具有栅偏压补偿的MOS晶体管电路",
        [
            "1.\n一种具有栅偏压补偿的MOS晶体管电路，其特征在于，至少包括：",
            "电阻器元件；",
            "MOS半导体组件，包括第一MOS半导体元件和第二MOS半导体元件；",
            "其中，所述电阻器元件与所述第一MOS半导体元件串联连接，所述第二MOS半导体元件通过栅极与所述电阻器元件和所述第一MOS半导体元件连接。",
        ],
    )
    assert claim_items[7] == m.Claim(
        8,
        "根据权利要求7所述的MOS晶体管电路",
        [
            "8.根据权利要求7所述的MOS晶体管电路，其特征在于：所述电阻器元件为多晶硅电阻。"
        ],
    )


def test_dependencies_list():
    pass

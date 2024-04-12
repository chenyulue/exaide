import pytest
import exaide.model as m
from collections.abc import Iterator


@pytest.fixture
def claim_model(claim):
    return m.ClaimModel(claim)


def test_claims_has_content(claim_model, claim):
    assert claim_model._claim == claim
    assert claim_model._sensitive_words == []


def test_split_claims(claim_model):
    claim_iter = claim_model.split_claims()
    assert isinstance(claim_iter, Iterator)

    claim_items = list(claim_iter)
    assert len(claim_items) == 10
    assert claim_items[1] == m.Claim(
        2,
        "根据权利要求1所述的MOS晶体管电路",
        "2.根据权利要求1所述的MOS晶体管电路，其特征在于：所述电阻器元件为上拉电阻或下拉电阻。",
        (144, 189),
    )
    assert claim_items[0] == m.Claim(
        1,
        "一种具有栅偏压补偿的MOS晶体管电路",
        "\n".join(
            [
                "1.\n一种具有栅偏压补偿的MOS晶体管电路，其特征在于，至少包括：",
                "电阻器元件；",
                "MOS半导体组件，包括第一MOS半导体元件和第二MOS半导体元件；",
                "其中，所述电阻器元件与所述第一MOS半导体元件串联连接，所述第二MOS半导体元件通过栅极与所述电阻器元件和所述第一MOS半导体元件连接。",
            ]
        ),
        (0, 143),
    )
    assert claim_items[7] == m.Claim(
        8,
        "根据权利要求7所述的MOS晶体管电路",
        "8.根据权利要求7所述的MOS晶体管电路，其特征在于：所述电阻器元件为多晶硅电阻。",
        (806, 847),
    )


@pytest.mark.parametrize(
    "num, expected",
    [
        (1, []),
        (2, [1]),
        (3, [1, 2]),
        (4, [3]),
        (5, [1, 2]),
        (6, [5]),
        (7, [1, 2, 3, 4, 5, 6]),
        (8, [7]),
        (9, [1, 2, 3, 4, 5, 6, 7, 8]),
        (10, [9]),
    ],
)
def test_check_dependencies(claim_model, num, expected):
    assert claim_model.claims[num].direct_dependencies == expected


@pytest.mark.parametrize(
    "num, expected",
    [
        (1, []),
        (2, [1]),
        (3, [1, 2]),
        (4, [1, 2, 3]),
        (5, [1, 2]),
        (6, [1, 2, 5]),
        (7, [1, 2, 3, 4, 5, 6]),
        (8, [1, 2, 3, 4, 5, 6, 7]),
        (9, [1, 2, 3, 4, 5, 6, 7, 8]),
    ],
)
def test_get_full_deps_path(claim_model, num, expected):
    assert claim_model._get_full_deps_path(num) == expected


@pytest.mark.parametrize(
    "num, expected",
    [
        (1, False),
        (2, True),
        (5, True),
        (8, True),
        (9, False),
        (10, True),
    ],
)
def test_is_subordinate(claim_model, num, expected):
    assert claim_model._is_subordinate(num)[0] == expected


@pytest.mark.parametrize(
    "num, expected",
    [
        (1, []),
        (2, [1]),
        (5, [1, 2]),
        (9, []),
        (10, [9]),
    ],
)
def test_get_actual_deps_path(claim_model, num, expected):
    assert claim_model._get_actual_deps_path(num) == expected


def test_get_actual_deps_with_other_sample(claims):
    cm = m.ClaimModel(claims[0])
    assert cm.claims[6].actual_dependencies == [7]
    assert cm.claims[7].actual_dependencies == []
    assert cm.claims[6].full_dependencies == [7]


def test_check_claim_defect(claim_model, claims):
    assert claim_model.claim_issue == m.ClaimIssue(
        multiple_subordinate_as_basis={7: [3, 5]},  # type: ignore
    )
    cm = m.ClaimModel(claims[0])
    assert cm.claim_issue == m.ClaimIssue(
        multiple_subordinate_as_basis={5: [3]},  # type: ignore
        subordinate_not_in_selected_form=[5, 7],
        subject_title_not_consistent={1: [10], 7: [6, 8]},  # type: ignore
        quotes_self_or_postclaim={6: [7]},   # type: ignore
    )

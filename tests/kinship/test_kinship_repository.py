"""Integration tests cho shortestPath; tự skip nếu chưa có seed data."""

import pytest

from core.neo4j_connection import run_read
from features.kinship import repository


@pytest.fixture
def seeded_neo4j(neo4j_ready):
    count = run_read(
        "MATCH (p:Person) WHERE p.id IN ['P011', 'P014'] RETURN count(p) AS count"
    )[0]["count"]
    if count != 2:
        pytest.skip("Neo4j chưa có dữ liệu seed P011/P014")


def test_shortest_path_between_cousins(seeded_neo4j):
    result = repository.find_shortest_path("P011", "P014")
    assert result is not None
    assert result["nodes"][0]["id"] == "P011"
    assert result["nodes"][-1]["id"] == "P014"
    assert len(result["relationships"]) == 4


def test_shortest_path_not_found(seeded_neo4j):
    assert repository.find_shortest_path("P011", "PERSON_KHONG_TON_TAI") is None


def test_shortest_path_respects_max_depth(seeded_neo4j):
    assert repository.find_shortest_path("P011", "P014", max_depth=3) is None
    assert repository.find_shortest_path("P011", "P014", max_depth=4) is not None


@pytest.mark.parametrize("depth", [0, 21, -1, 2.5, True])
def test_shortest_path_rejects_invalid_depth(depth):
    with pytest.raises(ValueError):
        repository.find_shortest_path("P011", "P014", max_depth=depth)

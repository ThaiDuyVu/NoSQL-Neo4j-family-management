"""
============================================================
FEATURE OWNER: SƠN — TEST: RELATIONSHIP REPOSITORY (integration, cần Neo4j)
============================================================
Dùng fixture neo4j_ready. Dùng id test riêng và dọn dữ liệu sau test.
"""
import pytest

TODO = "TODO (Sơn): implement"


@pytest.mark.skip(reason=TODO)
def test_create_and_delete_relationship(neo4j_ready):
    """create_relationship rồi delete_relationship."""


@pytest.mark.skip(reason=TODO)
def test_create_relationship_is_idempotent(neo4j_ready):
    """Gọi create 2 lần không sinh 2 relationship."""


@pytest.mark.skip(reason=TODO)
def test_count_parents(neo4j_ready):
    """count_parents trả đúng số cha/mẹ."""


@pytest.mark.skip(reason=TODO)
def test_is_ancestor(neo4j_ready):
    """is_ancestor đúng với chuỗi nhiều đời."""

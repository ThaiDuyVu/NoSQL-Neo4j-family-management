"""
============================================================
FEATURE OWNER: VŨ — TEST: PERSON REPOSITORY (integration, cần Neo4j)
============================================================
Dùng fixture neo4j_ready (tests/conftest.py). Nên dùng id test riêng (vd "TEST_...")
và dọn dữ liệu test sau mỗi test, đừng đụng dữ liệu seed.
"""
import pytest

TODO = "TODO (Vũ): implement"


@pytest.mark.skip(reason=TODO)
def test_create_and_find_by_id(neo4j_ready):
    """create_person rồi find_by_id."""


@pytest.mark.skip(reason=TODO)
def test_unique_constraint_on_id(neo4j_ready):
    """Tạo 2 Person trùng id -> lỗi từ constraint."""


@pytest.mark.skip(reason=TODO)
def test_count_all_and_by_gender(neo4j_ready):
    """count_all, count_by_gender khớp dữ liệu."""


@pytest.mark.skip(reason=TODO)
def test_delete_person(neo4j_ready):
    """delete_person xóa đúng node."""

"""
============================================================
FEATURE OWNER: ĐẠT — TEST: KINSHIP REPOSITORY (integration, cần Neo4j + seed)
============================================================
Chạy trên dữ liệu seed: python -m database.seed_data --reset
"""
import pytest

TODO = "TODO (Đạt): implement"


@pytest.mark.skip(reason=TODO)
def test_shortest_path_between_cousins(neo4j_ready):
    """P011 (Phúc) và P014 (Thành): path đi qua ông nội P001."""


@pytest.mark.skip(reason=TODO)
def test_shortest_path_not_found(neo4j_ready):
    """Hai Person không nối với nhau -> None."""


@pytest.mark.skip(reason=TODO)
def test_shortest_path_respects_max_depth(neo4j_ready):
    """max_depth nhỏ -> không tìm thấy path dài."""

"""
============================================================
SHARED FILE - CẢ NHÓM
============================================================
Fixture dùng chung cho test.

- neo4j_ready: skip test integration nếu chưa bật Neo4j (docker compose up -d).
Test của từng người nằm trong thư mục riêng: tests/person, tests/relationship, tests/kinship.
============================================================
"""
import pytest

from core.neo4j_connection import verify_connection


@pytest.fixture(scope="session")
def neo4j_ready():
    ok, message = verify_connection()
    if not ok:
        pytest.skip(f"Neo4j chưa sẵn sàng: {message}")

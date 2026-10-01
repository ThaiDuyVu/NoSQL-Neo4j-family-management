"""
============================================================
FEATURE OWNER: VŨ — TEST: PERSON SERVICE
============================================================
Unit test cho features/person/service.py.
Gợi ý: mock features.person.repository (monkeypatch) để không cần Neo4j.
"""
import pytest

TODO = "TODO (Vũ): implement"


@pytest.mark.skip(reason=TODO)
def test_create_person_success():
    """Tạo person hợp lệ -> trả về dict có id."""


@pytest.mark.skip(reason=TODO)
def test_create_person_duplicate_id():
    """Trùng id -> báo lỗi rõ ràng."""


@pytest.mark.skip(reason=TODO)
def test_create_person_empty_name():
    """full_name rỗng -> lỗi validation."""


@pytest.mark.skip(reason=TODO)
def test_create_person_invalid_gender():
    """gender không thuộc MALE/FEMALE -> lỗi."""


@pytest.mark.skip(reason=TODO)
def test_create_person_future_birth_date():
    """birth_date ở tương lai -> lỗi."""


@pytest.mark.skip(reason=TODO)
def test_update_person_not_found():
    """Update person không tồn tại -> lỗi."""


@pytest.mark.skip(reason=TODO)
def test_delete_person_not_found():
    """Delete person không tồn tại -> lỗi."""


@pytest.mark.skip(reason=TODO)
def test_search_persons_by_keyword_and_gender():
    """Tìm theo tên + lọc giới tính."""

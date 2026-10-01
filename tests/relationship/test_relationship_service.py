"""
============================================================
FEATURE OWNER: SƠN — TEST: RELATIONSHIP SERVICE
============================================================
Gợi ý: monkeypatch features.person.service.get_person và features.relationship.repository
để test validation không cần Neo4j.
"""
import pytest

TODO = "TODO (Sơn): implement"


@pytest.mark.skip(reason=TODO)
def test_add_father_of_success():
    """Cha MALE -> con: tạo thành công."""


@pytest.mark.skip(reason=TODO)
def test_father_must_be_male():
    """FATHER_OF với người FEMALE -> lỗi."""


@pytest.mark.skip(reason=TODO)
def test_mother_must_be_female():
    """MOTHER_OF với người MALE -> lỗi."""


@pytest.mark.skip(reason=TODO)
def test_cannot_relate_to_self():
    """from_id == to_id -> lỗi."""


@pytest.mark.skip(reason=TODO)
def test_child_cannot_have_two_fathers():
    """Con đã có cha, thêm cha thứ 2 -> lỗi."""


@pytest.mark.skip(reason=TODO)
def test_no_ancestor_cycle():
    """A là cha B, thêm B là cha A -> lỗi vòng lặp."""


@pytest.mark.skip(reason=TODO)
def test_duplicate_relationship_rejected():
    """Thêm lại relationship đã có -> lỗi."""


@pytest.mark.skip(reason=TODO)
def test_spouse_rules():
    """SPOUSE_OF: giới hạn số vợ/chồng, không phải cha/mẹ/con của nhau."""


@pytest.mark.skip(reason=TODO)
def test_unknown_person_rejected():
    """Person không tồn tại -> lỗi."""

"""
============================================================
FEATURE OWNER: ĐẠT — TEST: KINSHIP SERVICE & RELATIONSHIP SEARCH
============================================================
Gợi ý: monkeypatch search_service.search_relationship_path và person_service.get_person.
"""
import pytest

TODO = "TODO (Đạt): implement"


@pytest.mark.skip(reason=TODO)
def test_find_kinship_no_path():
    """Hai người không liên quan -> found=False, có message."""


@pytest.mark.skip(reason=TODO)
def test_find_kinship_same_person():
    """A == B -> xử lý rõ ràng."""


@pytest.mark.skip(reason=TODO)
def test_build_steps_direction():
    """build_steps_from_raw_path xác định đúng UP / DOWN / SPOUSE."""


@pytest.mark.skip(reason=TODO)
def test_format_path_text():
    """Chuỗi đường đi dễ đọc."""

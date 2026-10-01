"""
============================================================
FEATURE OWNER: ĐẠT — TEST: KINSHIP RESOLVER (không cần Neo4j)
============================================================
Dựng list[PathStep] giả rồi gọi resolver.resolve_kinship.
Mỗi case: A gọi B là gì + B gọi A là gì.
Dữ liệu mẫu tham chiếu: database/seed_data.py, docs/DEMO_FLOW.md.
"""
import pytest

TODO = "TODO (Đạt): implement"

CASES = [
    "Cha / Mẹ / Con trai / Con gái",
    "Ông nội / Bà nội / Ông ngoại / Bà ngoại",
    "Anh / Chị / Em (cùng cha mẹ, dựa vào ngày sinh)",
    "Anh/chị/em họ",
    "Bác / Chú / Cô (bên nội)",
    "Cậu / Dì (bên ngoại)",
    "Vợ / Chồng",
    "Cháu",
    "Cụ",
]


@pytest.mark.skip(reason=TODO)
@pytest.mark.parametrize("case", CASES)
def test_resolve_supported_terms(case):
    """Mỗi nhóm quan hệ: kiểm tra a_calls_b và b_calls_a."""


@pytest.mark.skip(reason=TODO)
def test_resolve_same_person():
    """A == B -> xử lý rõ ràng."""


@pytest.mark.skip(reason=TODO)
def test_resolve_missing_birth_date():
    """Thiếu birth_date khi cần so sánh tuổi -> hành vi mặc định đã thống nhất."""


@pytest.mark.skip(reason=TODO)
def test_resolve_unsupported_path():
    """Path quá xa/không hỗ trợ -> found=True nhưng message rõ ràng (hoặc quy ước khác)."""

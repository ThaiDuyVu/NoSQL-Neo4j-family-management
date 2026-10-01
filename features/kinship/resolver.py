"""
============================================================
FEATURE OWNER: ĐẠT
DOMAIN: KINSHIP RESOLVER
============================================================

Responsibilities:
- Chuyển đường đi quan hệ (path) thành CÁCH XƯNG HÔ tiếng Việt
- Thuần logic: KHÔNG gọi database, KHÔNG import streamlit
  (để test được bằng dữ liệu giả)

============================================================
"""
from dataclasses import dataclass, field
from typing import Optional

# Từ vựng cần hỗ trợ (xem docs/MEMBER_DAT.md)
SUPPORTED_TERMS = [
    "Cha", "Mẹ", "Con trai", "Con gái",
    "Ông nội", "Bà nội", "Ông ngoại", "Bà ngoại",
    "Anh", "Chị", "Em", "Anh/chị/em họ",
    "Bác", "Chú", "Cô", "Cậu", "Dì",
    "Vợ", "Chồng", "Cháu", "Cụ",
]


@dataclass
class PathStep:
    """Một bước trên đường đi từ A đến B."""
    from_id: str
    to_id: str
    rel_type: str            # FATHER_OF | MOTHER_OF | SPOUSE_OF
    direction: str           # "UP" (đi lên cha/mẹ) | "DOWN" (đi xuống con) | "SPOUSE"
    from_gender: str = ""
    to_gender: str = ""
    from_birth_date: Optional[str] = None
    to_birth_date: Optional[str] = None


@dataclass
class KinshipResult:
    found: bool
    person_a_id: str = ""
    person_b_id: str = ""
    a_calls_b: str = ""      # A gọi B là ...
    b_calls_a: str = ""      # B gọi A là ...
    path_text: str = ""      # mô tả đường đi
    steps: list[PathStep] = field(default_factory=list)
    message: str = ""        # thông báo (vd: không tìm thấy quan hệ)


def classify_path(steps: list[PathStep]) -> str:
    """
    OWNER: Đạt

    TODO:
    - biến list step thành "pattern" dễ so khớp, ví dụ "UP,UP,DOWN" hoặc "UP,SPOUSE"
    - quyết định cách biểu diễn pattern (thống nhất trong team test)
    """
    raise NotImplementedError


def resolve_kinship(steps: list[PathStep], a_gender: str, b_gender: str) -> KinshipResult:
    """
    OWNER: Đạt

    TODO:
    - phân tích pattern (classify_path)
    - xác định bên nội / bên ngoại (đi lên qua FATHER_OF hay MOTHER_OF)
    - xác định anh/chị/em, bác/chú, cô/cậu/dì dựa trên giới tính + ngày sinh
    - trả KinshipResult với a_calls_b và b_calls_a
    - xử lý path rỗng (A == B) và trường hợp không hỗ trợ
    """
    raise NotImplementedError


def compare_age(birth_date_a: Optional[str], birth_date_b: Optional[str]) -> int:
    """
    OWNER: Đạt

    TODO:
    - trả -1 / 0 / 1 (A lớn hơn / bằng / nhỏ hơn B) hoặc quy ước khác
    - xử lý thiếu birth_date (quyết định hành vi mặc định, ghi vào docs)
    """
    raise NotImplementedError

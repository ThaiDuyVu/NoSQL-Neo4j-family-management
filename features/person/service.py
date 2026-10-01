"""
============================================================
FEATURE OWNER: VŨ
DOMAIN: PERSON MANAGEMENT
============================================================

Responsibilities:
- CRUD Person
- Search Person
- Validation Person
- Public interface cho feature khác (Sơn, Đạt gọi qua file này,
  KHÔNG import person.repository)

PUBLIC INTERFACE (đừng đổi signature khi chưa báo nhóm):
- list_persons(skip, limit) -> list[dict]
- get_person(person_id)     -> dict | None
- search_persons(keyword, gender) -> list[dict]
Person dict có key: id, full_name, gender, birth_date, address, phone, note

============================================================
"""
from typing import Optional

from features.person import repository  # noqa: F401


# ---------------- PUBLIC INTERFACE (Sơn / Đạt dùng) ----------------

def list_persons(skip: int = 0, limit: int = 100) -> list[dict]:
    """
    OWNER: Vũ

    TODO:
    - gọi repository.find_all
    - Sơn/Đạt dùng hàm này để đổ dữ liệu vào selectbox
    """
    raise NotImplementedError


def get_person(person_id: str) -> Optional[dict]:
    """OWNER: Vũ — TODO: gọi repository.find_by_id; None nếu không có."""
    raise NotImplementedError


def search_persons(keyword: str = "", gender: Optional[str] = None) -> list[dict]:
    """OWNER: Vũ — TODO: chuẩn hóa keyword, validate gender, gọi repository.search_by_keyword."""
    raise NotImplementedError


# ---------------- CRUD ----------------

def create_person(
    id: str,
    full_name: str,
    gender: str,
    birth_date: Optional[str] = None,
    address: Optional[str] = None,
    phone: Optional[str] = None,
    note: Optional[str] = None,
) -> dict:
    """
    OWNER: Vũ

    TODO:
    - validate input (validate_person_input)
    - kiểm tra duplicate id
    - call repository
    - handle duplicate id
    """
    raise NotImplementedError


def update_person(person_id: str, **changes) -> dict:
    """
    OWNER: Vũ

    TODO:
    - kiểm tra person tồn tại
    - validate các field thay đổi
    - không cho đổi id
    - call repository.update_person
    """
    raise NotImplementedError


def delete_person(person_id: str) -> None:
    """
    OWNER: Vũ

    TODO:
    - kiểm tra person tồn tại
    - quyết định chính sách khi person còn relationship
    - call repository.delete_person
    """
    raise NotImplementedError


# ---------------- Statistics (Dashboard dùng) ----------------

def get_statistics() -> dict:
    """
    OWNER: Vũ

    TODO:
    - trả {"total": int, "male": int, "female": int}
    - gọi repository.count_all / count_by_gender
    """
    raise NotImplementedError


# ---------------- Validation ----------------

def validate_person_input(data: dict, is_update: bool = False) -> list[str]:
    """
    OWNER: Vũ

    TODO:
    - id không rỗng (khi tạo)
    - full_name không rỗng
    - gender thuộc GENDERS
    - birth_date đúng ISO, không ở tương lai
    - trả về danh sách thông báo lỗi (rỗng = hợp lệ) hoặc raise ValueError — thống nhất 1 cách
    - có thể dùng shared/validators.py
    """
    raise NotImplementedError

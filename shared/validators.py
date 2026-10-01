"""
============================================================
SHARED FILE - CẢ NHÓM
============================================================
Validator DÙNG CHUNG, không gắn với feature nào.
Validation nghiệp vụ riêng (Person / Relationship / Kinship)
phải nằm trong service của feature tương ứng.

Quy tắc:
- Hạn chế chỉnh nếu không cần.
- Không xóa code của thành viên khác.
- Thay đổi interface dùng chung phải báo nhóm.
============================================================
"""
from datetime import date
from typing import Optional

from core.constants import GENDERS


def is_blank(value: Optional[str]) -> bool:
    return value is None or not str(value).strip()


def is_valid_gender(value: Optional[str]) -> bool:
    return value in GENDERS


def is_valid_iso_date(value: Optional[str]) -> bool:
    """True nếu value có dạng YYYY-MM-DD hợp lệ."""
    try:
        date.fromisoformat(str(value))
        return True
    except ValueError:
        return False

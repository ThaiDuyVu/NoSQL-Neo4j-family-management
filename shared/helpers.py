"""
============================================================
SHARED FILE - CẢ NHÓM
============================================================
Hàm tiện ích nhỏ dùng chung.

Quy tắc:
- Hạn chế chỉnh nếu không cần.
- Không xóa code của thành viên khác.
- Thay đổi interface dùng chung phải báo nhóm.
- Không đặt business logic riêng của feature vào shared.
============================================================
"""
from typing import Any, Optional


def clean_str(value: Optional[str]) -> str:
    """Strip khoảng trắng; None -> ''."""
    return (value or "").strip()


def drop_none(data: dict[str, Any]) -> dict[str, Any]:
    """Bỏ các key có value None (hữu ích khi build params update)."""
    return {k: v for k, v in data.items() if v is not None}

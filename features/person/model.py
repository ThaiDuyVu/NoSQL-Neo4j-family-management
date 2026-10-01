"""
============================================================
FEATURE OWNER: VŨ
DOMAIN: PERSON MANAGEMENT
============================================================

Responsibilities:
- Định nghĩa model Person (dataclass)
- Chuyển đổi dict <-> Person

============================================================
"""
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Person:
    id: str
    full_name: str
    gender: str                      # "MALE" | "FEMALE"
    birth_date: Optional[str] = None  # ISO "YYYY-MM-DD"
    address: Optional[str] = None
    phone: Optional[str] = None
    note: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Person":
        # TODO (Vũ): lọc key lạ, xử lý thiếu field nếu cần
        return cls(**{k: data.get(k) for k in cls.__dataclass_fields__})

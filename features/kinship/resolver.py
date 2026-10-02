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
from datetime import date
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
    from_name: str = ""
    to_name: str = ""


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
    """Biến các bước thành pattern như ``UP,UP,DOWN`` để so khớp rule."""
    return ",".join(step.direction for step in steps)


def resolve_kinship(steps: list[PathStep], a_gender: str, b_gender: str) -> KinshipResult:
    """Xác định cách gọi hai chiều từ một path đã chuẩn hóa."""
    if not steps:
        return KinshipResult(
            found=False,
            message="Không thể xác định quan hệ khi hai người trùng nhau hoặc đường đi rỗng.",
        )

    a_calls_b = _resolve_one_direction(steps, b_gender)
    reversed_steps = [_reverse_step(step) for step in reversed(steps)]
    b_calls_a = _resolve_one_direction(reversed_steps, a_gender)

    unsupported = not a_calls_b or not b_calls_a
    return KinshipResult(
        found=True,
        a_calls_b=a_calls_b or "Chưa xác định",
        b_calls_a=b_calls_a or "Chưa xác định",
        steps=steps,
        message=(
            "Đã tìm thấy đường đi nhưng chưa hỗ trợ đầy đủ cách xưng hô này."
            if unsupported
            else ""
        ),
    )


def compare_age(birth_date_a: Optional[str], birth_date_b: Optional[str]) -> int:
    """Trả -1 nếu A lớn hơn, 1 nếu A nhỏ hơn, 0 nếu bằng/không xác định."""
    if not birth_date_a or not birth_date_b:
        return 0
    try:
        parsed_a = date.fromisoformat(birth_date_a)
        parsed_b = date.fromisoformat(birth_date_b)
    except (TypeError, ValueError):
        return 0
    if parsed_a < parsed_b:
        return -1
    if parsed_a > parsed_b:
        return 1
    return 0


def _reverse_step(step: PathStep) -> PathStep:
    direction = {"UP": "DOWN", "DOWN": "UP", "SPOUSE": "SPOUSE"}.get(
        step.direction,
        step.direction,
    )
    return PathStep(
        from_id=step.to_id,
        to_id=step.from_id,
        rel_type=step.rel_type,
        direction=direction,
        from_gender=step.to_gender,
        to_gender=step.from_gender,
        from_birth_date=step.to_birth_date,
        to_birth_date=step.from_birth_date,
        from_name=step.to_name,
        to_name=step.from_name,
    )


def _gendered(gender: str, male_term: str, female_term: str, neutral_term: str) -> str:
    if gender == "MALE":
        return male_term
    if gender == "FEMALE":
        return female_term
    return neutral_term


def _sibling_term(steps: list[PathStep], cousin: bool = False) -> str:
    source_birth = steps[0].from_birth_date
    target_birth = steps[-1].to_birth_date
    target_gender = steps[-1].to_gender
    age_order = compare_age(source_birth, target_birth)
    suffix = " họ" if cousin else ""

    if age_order < 0:
        return f"Em{suffix}"
    if age_order > 0:
        return _gendered(
            target_gender,
            f"Anh{suffix}",
            f"Chị{suffix}",
            f"Anh/chị{suffix}",
        )
    return "Anh/chị/em họ" if cousin else "Anh/chị/em"


def _aunt_or_uncle_term(steps: list[PathStep]) -> str:
    # Bên nội/ngoại được xác định bởi cha/mẹ mà A đi lên ở bước đầu.
    is_paternal = steps[0].rel_type == "FATHER_OF"
    parent_birth = steps[0].to_birth_date
    relative_birth = steps[-1].to_birth_date
    relative_gender = steps[-1].to_gender
    relative_age = compare_age(relative_birth, parent_birth)

    if relative_age < 0:
        return "Bác"
    if is_paternal:
        if relative_age == 0:
            return _gendered(relative_gender, "Bác/chú", "Bác/cô", "Bác/chú/cô")
        return _gendered(relative_gender, "Chú", "Cô", "Chú/cô")
    if relative_age == 0:
        return _gendered(relative_gender, "Bác/cậu", "Bác/dì", "Bác/cậu/dì")
    return _gendered(relative_gender, "Cậu", "Dì", "Cậu/dì")


def _resolve_one_direction(steps: list[PathStep], target_gender: str) -> str:
    pattern = classify_path(steps)

    if pattern == "SPOUSE":
        return _gendered(target_gender, "Chồng", "Vợ", "Vợ/chồng")

    if pattern == "UP":
        if steps[0].rel_type == "FATHER_OF":
            return "Cha"
        if steps[0].rel_type == "MOTHER_OF":
            return "Mẹ"
        return ""

    if pattern == "DOWN":
        return _gendered(target_gender, "Con trai", "Con gái", "Con")

    if pattern == "UP,DOWN":
        return _sibling_term(steps)

    if pattern == "UP,UP":
        side = "nội" if steps[0].rel_type == "FATHER_OF" else "ngoại"
        return _gendered(target_gender, f"Ông {side}", f"Bà {side}", f"Ông/bà {side}")

    if pattern == "DOWN,DOWN":
        return "Cháu"

    if pattern == "UP,UP,DOWN":
        return _aunt_or_uncle_term(steps)

    if pattern == "UP,DOWN,DOWN":
        return "Cháu"

    if pattern == "UP,UP,DOWN,DOWN":
        return _sibling_term(steps, cousin=True)

    directions = [step.direction for step in steps]
    if len(directions) >= 3 and all(direction == "UP" for direction in directions):
        return "Cụ"
    if len(directions) >= 3 and all(direction == "DOWN" for direction in directions):
        return "Cháu"

    return ""

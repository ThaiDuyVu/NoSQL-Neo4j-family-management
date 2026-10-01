"""Person business rules and public interface for other features."""
from datetime import date
from typing import Optional

from neo4j.exceptions import ConstraintError, Neo4jError

from core.constants import GENDERS, PERSON_FIELDS
from features.person import repository
from shared.validators import is_blank


def list_persons(skip: int = 0, limit: int = 100) -> list[dict]:
    if skip < 0 or limit < 0:
        raise ValueError("skip và limit phải không âm")
    return repository.find_all(skip, limit)


def get_person(person_id: str) -> Optional[dict]:
    return repository.find_by_id(person_id.strip()) if person_id and person_id.strip() else None


def search_persons(keyword: str = "", gender: Optional[str] = None) -> list[dict]:
    if gender is not None and gender not in GENDERS:
        raise ValueError("Giới tính phải là MALE hoặc FEMALE")
    return repository.search_by_keyword((keyword or "").strip(), gender)


def create_person(
    id: str,
    full_name: str,
    gender: str,
    birth_date: Optional[str] = None,
    address: Optional[str] = None,
    phone: Optional[str] = None,
    note: Optional[str] = None,
) -> dict:
    data = {
        "id": id.strip() if isinstance(id, str) else id,
        "full_name": full_name.strip() if isinstance(full_name, str) else full_name,
        "gender": gender,
        "birth_date": birth_date,
        "address": address,
        "phone": phone,
        "note": note,
    }
    errors = validate_person_input(data)
    if errors:
        raise ValueError("; ".join(errors))
    if repository.exists_by_id(data["id"]):
        raise ValueError(f"ID {data['id']} đã tồn tại")
    try:
        return repository.create_person(data)
    except ConstraintError as exc:
        # A second writer may create the same ID after the existence check.
        raise ValueError(f"ID {data['id']} đã tồn tại") from exc


def update_person(person_id: str, **changes) -> dict:
    if not person_id or not person_id.strip():
        raise ValueError("ID không được để trống")
    person_id = person_id.strip()
    if "id" in changes:
        raise ValueError("Không thể đổi ID")
    unknown = set(changes) - set(PERSON_FIELDS)
    if unknown:
        raise ValueError(f"Trường không hợp lệ: {', '.join(sorted(unknown))}")
    current = repository.find_by_id(person_id)
    if current is None:
        raise ValueError(f"Không tìm thấy Person {person_id}")
    errors = validate_person_input(changes, is_update=True)
    if errors:
        raise ValueError("; ".join(errors))
    if "full_name" in changes:
        changes["full_name"] = changes["full_name"].strip()
    updated = repository.update_person(person_id, changes)
    if updated is None:
        raise ValueError(f"Không tìm thấy Person {person_id}")
    return updated


def delete_person(person_id: str) -> None:
    if not get_person(person_id):
        raise ValueError(f"Không tìm thấy Person {person_id}")
    try:
        deleted = repository.delete_person(person_id.strip())
    except Neo4jError as exc:
        if isinstance(exc, ConstraintError) or "still has relationships" in str(exc).lower():
            raise ValueError("Không thể xóa Person đang có quan hệ gia đình") from exc
        raise
    if not deleted:
        raise ValueError(f"Không tìm thấy Person {person_id}")


def get_statistics() -> dict:
    counts = repository.count_by_gender()
    return {
        "total": repository.count_all(),
        "male": counts.get("MALE", 0),
        "female": counts.get("FEMALE", 0),
    }


def validate_person_input(data: dict, is_update: bool = False) -> list[str]:
    errors = []
    if not is_update or "id" in data:
        if is_blank(data.get("id")):
            errors.append("ID không được để trống")
    if not is_update or "full_name" in data:
        if is_blank(data.get("full_name")):
            errors.append("Họ tên không được để trống")
    if not is_update or "gender" in data:
        if data.get("gender") not in GENDERS:
            errors.append("Giới tính phải là MALE hoặc FEMALE")
    if "birth_date" in data and data["birth_date"] not in (None, ""):
        value = data["birth_date"]
        try:
            if not isinstance(value, str) or len(value) != 10 or date.fromisoformat(value).isoformat() != value:
                raise ValueError
            if date.fromisoformat(value) > date.today():
                errors.append("Ngày sinh không được ở tương lai")
        except ValueError:
            errors.append("Ngày sinh phải theo định dạng YYYY-MM-DD hợp lệ")
    return errors

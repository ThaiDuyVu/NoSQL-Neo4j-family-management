"""Person service unit tests without a database."""
from datetime import date, timedelta

import pytest

from features.person import service


@pytest.fixture
def store(monkeypatch):
    people = {}
    monkeypatch.setattr(service.repository, "exists_by_id", lambda id: id in people)
    monkeypatch.setattr(service.repository, "find_by_id", lambda id: people.get(id))
    monkeypatch.setattr(service.repository, "create_person", lambda person: people.setdefault(person["id"], person))
    monkeypatch.setattr(service.repository, "update_person", lambda id, changes: people[id].update(changes) or people[id])
    monkeypatch.setattr(service.repository, "delete_person", lambda id: people.pop(id, None) is not None)
    monkeypatch.setattr(service.repository, "find_all", lambda skip, limit: list(people.values())[skip:skip + limit])
    monkeypatch.setattr(service.repository, "search_by_keyword", lambda keyword, gender: [
        p for p in people.values()
        if (keyword.lower() in p["full_name"].lower() or keyword.lower() in p["id"].lower())
        and (gender is None or p["gender"] == gender)
    ])
    return people


def test_create_person_success(store):
    assert service.create_person(" P001 ", " An ", "MALE")["full_name"] == "An"
    assert service.get_person("P001")["id"] == "P001"
    assert len(service.list_persons()) == 1


def test_create_person_duplicate_id(store):
    service.create_person("P001", "An", "MALE")
    with pytest.raises(ValueError, match="đã tồn tại"):
        service.create_person("P001", "Bình", "FEMALE")


def test_create_person_empty_name(store):
    with pytest.raises(ValueError, match="Họ tên"):
        service.create_person("P001", "  ", "MALE")


def test_create_person_invalid_gender(store):
    with pytest.raises(ValueError, match="Giới tính"):
        service.create_person("P001", "An", "OTHER")


def test_create_person_future_birth_date(store):
    future = (date.today() + timedelta(days=1)).isoformat()
    with pytest.raises(ValueError, match="tương lai"):
        service.create_person("P001", "An", "MALE", future)


def test_create_person_invalid_birth_date(store):
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        service.create_person("P001", "An", "MALE", "2024-02-30")


def test_update_person_not_found(store):
    with pytest.raises(ValueError, match="Không tìm thấy"):
        service.update_person("P999", full_name="An")


def test_update_person_validation_and_id_immutable(store):
    service.create_person("P001", "An", "MALE")
    with pytest.raises(ValueError, match="Không thể đổi ID"):
        service.update_person("P001", id="P002")
    with pytest.raises(ValueError, match="Họ tên"):
        service.update_person("P001", full_name=" ")
    assert service.update_person("P001", full_name="Bình")["full_name"] == "Bình"


def test_delete_person_not_found(store):
    with pytest.raises(ValueError, match="Không tìm thấy"):
        service.delete_person("P999")


def test_search_persons_by_keyword_and_gender(store):
    service.create_person("P001", "An", "MALE")
    service.create_person("P002", "Anh", "FEMALE")
    assert [p["id"] for p in service.search_persons(" AN ", "FEMALE")] == ["P002"]
    assert [p["id"] for p in service.search_persons("p001")] == ["P001"]
    with pytest.raises(ValueError, match="Giới tính"):
        service.search_persons("", "OTHER")

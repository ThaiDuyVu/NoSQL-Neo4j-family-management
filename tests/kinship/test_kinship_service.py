"""Unit tests cho orchestration service và chuyển đổi raw path."""

from features.kinship import service as kinship_service
from features.kinship.resolver import PathStep
from features.relationship_search import service as search_service


PEOPLE = {
    "A": {"id": "A", "full_name": "Người A", "gender": "MALE", "birth_date": "2000-01-01"},
    "B": {"id": "B", "full_name": "Người B", "gender": "MALE", "birth_date": "1970-01-01"},
}


def test_find_kinship_no_path(monkeypatch):
    monkeypatch.setattr(kinship_service.person_service, "get_person", lambda person_id: PEOPLE.get(person_id))
    monkeypatch.setattr(kinship_service.search_service, "search_relationship_path", lambda *_: None)
    result = kinship_service.find_kinship("A", "B")
    assert result.found is False
    assert "Không tìm thấy đường đi" in result.message


def test_find_kinship_same_person_does_not_query(monkeypatch):
    def fail(_):
        raise AssertionError("Không được query khi A == B")

    monkeypatch.setattr(kinship_service.person_service, "get_person", fail)
    result = kinship_service.find_kinship("A", "A")
    assert result.found is False
    assert "hai người khác nhau" in result.message


def test_find_kinship_orchestrates_and_formats(monkeypatch):
    step = PathStep(
        "A", "B", "FATHER_OF", "UP",
        from_gender="MALE", to_gender="MALE",
        from_birth_date="2000-01-01", to_birth_date="1970-01-01",
        from_name="Người A", to_name="Người B",
    )
    monkeypatch.setattr(kinship_service.person_service, "get_person", lambda person_id: PEOPLE.get(person_id))
    monkeypatch.setattr(kinship_service.search_service, "search_relationship_path", lambda *_: [step])
    result = kinship_service.find_kinship("A", "B")
    assert result.found is True
    assert result.a_calls_b == "Cha"
    assert result.b_calls_a == "Con trai"
    assert result.path_text == "Người A → (con của) Người B"


def test_list_selectable_persons_is_sorted(monkeypatch):
    monkeypatch.setattr(
        kinship_service.person_service,
        "list_persons",
        lambda limit: [
            {"id": "2", "full_name": "Bình"},
            {"id": "1", "full_name": "An"},
        ],
    )
    assert [person["id"] for person in kinship_service.list_selectable_persons()] == ["1", "2"]


def test_build_steps_direction():
    raw_path = {
        "nodes": [
            {"id": "A", "full_name": "A", "gender": "MALE", "birth_date": "2000-01-01"},
            {"id": "B", "full_name": "B", "gender": "MALE", "birth_date": "1970-01-01"},
            {"id": "C", "full_name": "C", "gender": "FEMALE", "birth_date": "1972-01-01"},
            {"id": "D", "full_name": "D", "gender": "FEMALE", "birth_date": "2002-01-01"},
        ],
        "relationships": [
            {"type": "FATHER_OF", "start_id": "B", "end_id": "A"},
            {"type": "SPOUSE_OF", "start_id": "B", "end_id": "C"},
            {"type": "MOTHER_OF", "start_id": "C", "end_id": "D"},
        ],
    }
    steps = search_service.build_steps_from_raw_path(raw_path, "A")
    assert [step.direction for step in steps] == ["UP", "SPOUSE", "DOWN"]
    assert steps[0].from_name == "A"
    assert steps[-1].to_name == "D"


def test_build_steps_reverses_raw_path_when_needed():
    raw_path = {
        "nodes": [{"id": "B"}, {"id": "A"}],
        "relationships": [{"type": "FATHER_OF", "start_id": "B", "end_id": "A"}],
    }
    steps = search_service.build_steps_from_raw_path(raw_path, "A")
    assert [(step.from_id, step.to_id, step.direction) for step in steps] == [("A", "B", "UP")]


def test_format_path_text():
    steps = [
        PathStep("A", "B", "FATHER_OF", "UP"),
        PathStep("B", "C", "FATHER_OF", "UP"),
    ]
    people = {
        "A": {"full_name": "Phúc"},
        "B": {"full_name": "Dũng"},
        "C": {"full_name": "An"},
    }
    assert search_service.format_path_text(steps, people) == (
        "Phúc → (con của) Dũng → (con của) An"
    )

import pytest
from features.relationship.service import RelationshipService, RELATIONSHIP_TYPES


@pytest.fixture
def mock_deps(mocker):
    mock_repo = mocker.Mock()
    mock_person_svc = mocker.Mock()
    service = RelationshipService(repo=mock_repo, person_service=mock_person_svc)
    return service, mock_repo, mock_person_svc


def test_add_relationship_success(mock_deps):
    service, mock_repo, mock_person_svc = mock_deps

    mock_person_svc.get_person.side_effect = lambda pid: {
        "P1": {"id": "P1", "name": "Cha", "gender": "MALE"},
        "P2": {"id": "P2", "name": "Con", "gender": "FEMALE"}
    }.get(pid)

    mock_repo.relationship_exists.return_value = False
    mock_repo.count_parents.return_value = {"father_count": 0, "mother_count": 0}
    mock_repo.is_ancestor.return_value = False
    mock_repo.create_relationship.return_value = True

    rel_type = RELATIONSHIP_TYPES.get("FATHER_OF", "FATHER_OF")
    result = service.add_relationship("P1", "P2", rel_type)
    assert result is True


def test_self_relationship_error(mock_deps):
    service, _, _ = mock_deps
    rel_type = RELATIONSHIP_TYPES.get("FATHER_OF", "FATHER_OF")
    with pytest.raises(ValueError, match="Không thể tạo quan hệ với chính mình"):
        service.add_relationship("P1", "P1", rel_type)


def test_father_must_be_male(mock_deps):
    service, mock_repo, mock_person_svc = mock_deps
    mock_person_svc.get_person.side_effect = lambda pid: {
        "P1": {"id": "P1", "name": "Mẹ", "gender": "FEMALE"},
        "P2": {"id": "P2", "name": "Con", "gender": "MALE"}
    }.get(pid)

    mock_repo.relationship_exists.return_value = False

    rel_type = RELATIONSHIP_TYPES.get("FATHER_OF", "FATHER_OF")
    with pytest.raises(ValueError, match="Cha phải có giới tính là Nam"):
        service.add_relationship("P1", "P2", rel_type)


def test_multiple_fathers_error(mock_deps):
    service, mock_repo, mock_person_svc = mock_deps
    mock_person_svc.get_person.side_effect = lambda pid: {
        "P1": {"id": "P1", "name": "Cha2", "gender": "MALE"},
        "P2": {"id": "P2", "name": "Con", "gender": "MALE"}
    }.get(pid)

    mock_repo.relationship_exists.return_value = False
    mock_repo.count_parents.return_value = {"father_count": 1, "mother_count": 0}

    rel_type = RELATIONSHIP_TYPES.get("FATHER_OF", "FATHER_OF")
    with pytest.raises(ValueError, match="đã có cha"):
        service.add_relationship("P1", "P2", rel_type)


def test_ancestor_loop_error(mock_deps):
    service, mock_repo, mock_person_svc = mock_deps
    mock_person_svc.get_person.side_effect = lambda pid: {
        "P1": {"id": "P1", "name": "Ông", "gender": "MALE"},
        "P2": {"id": "P2", "name": "Cháu", "gender": "MALE"}
    }.get(pid)

    mock_repo.relationship_exists.return_value = False
    mock_repo.count_parents.return_value = {"father_count": 0, "mother_count": 0}
    mock_repo.is_ancestor.return_value = True

    rel_type = RELATIONSHIP_TYPES.get("FATHER_OF", "FATHER_OF")
    with pytest.raises(ValueError, match="vòng lặp tổ tiên"):
        service.add_relationship("P1", "P2", rel_type)


def test_spouse_rules(mock_deps):
    service, mock_repo, mock_person_svc = mock_deps
    mock_person_svc.get_person.side_effect = lambda pid: {
        "P1": {"id": "P1", "name": "Chồng", "gender": "MALE"},
        "P2": {"id": "P2", "name": "Vợ", "gender": "FEMALE"}
    }.get(pid)

    mock_repo.relationship_exists.return_value = False
    mock_repo.is_ancestor.return_value = False
    mock_repo.count_spouses.return_value = 1

    rel_type = RELATIONSHIP_TYPES.get("SPOUSE_OF", "SPOUSE_OF")
    with pytest.raises(ValueError, match="đã có hôn phối"):
        service.add_relationship("P1", "P2", rel_type)
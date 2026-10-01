import pytest
from features.relationship.repository import RelationshipRepository


@pytest.fixture
def repo(mocker):
    r = RelationshipRepository()
    mocker.patch.object(r, "_execute")
    return r


def test_validate_rel_type_invalid(repo):
    with pytest.raises(ValueError):
        repo._validate_rel_type("INVALID_TYPE")


def test_repository_methods_smoke(repo):
    repo._execute.return_value = [{"created": 1}]
    assert repo.create_relationship("P1", "P2", "FATHER_OF") is True

    repo._execute.return_value = [{"deleted": 1}]
    assert repo.delete_relationship("P1", "P2", "FATHER_OF") is True

    repo._execute.return_value = [{"exists": True}]
    assert repo.relationship_exists("P1", "P2", "SPOUSE_OF") is True
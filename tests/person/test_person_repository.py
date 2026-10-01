"""Person repository integration tests; run only when Neo4j is available."""
from uuid import uuid4

import pytest
from neo4j.exceptions import ConstraintError, Neo4jError

from core.neo4j_connection import run_write
from features.person import repository


@pytest.fixture
def test_id(neo4j_ready):
    person_id = "TEST_" + uuid4().hex
    try:
        yield person_id
    finally:
        run_write("MATCH (p:Person {id: $id}) DETACH DELETE p", {"id": person_id})


def person(person_id, gender="MALE"):
    return {"id": person_id, "full_name": "Test Person", "gender": gender,
            "birth_date": None, "address": None, "phone": None, "note": None}


def test_create_and_find_by_id(test_id):
    assert repository.create_person(person(test_id))["id"] == test_id
    assert repository.find_by_id(test_id)["full_name"] == "Test Person"
    assert repository.exists_by_id(test_id)
    assert repository.update_person(test_id, {"full_name": "Changed"})["full_name"] == "Changed"
    assert any(p["id"] == test_id for p in repository.search_by_keyword(test_id.lower()))


def test_unique_constraint_on_id(test_id):
    run_write("CREATE CONSTRAINT person_id_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE")
    repository.create_person(person(test_id))
    with pytest.raises(ConstraintError):
        repository.create_person(person(test_id))


def test_count_all_and_by_gender(test_id):
    before_total = repository.count_all()
    before_male = repository.count_by_gender()["MALE"]
    repository.create_person(person(test_id))
    assert repository.count_all() == before_total + 1
    assert repository.count_by_gender()["MALE"] == before_male + 1


def test_delete_person(test_id):
    repository.create_person(person(test_id))
    assert repository.delete_person(test_id)
    assert repository.find_by_id(test_id) is None
    assert not repository.delete_person(test_id)


def test_delete_person_with_relationship_is_blocked(test_id):
    repository.create_person(person(test_id))
    run_write("MATCH (p:Person {id: $id}) CREATE (p)-[:TEST_LINK]->(:Person {id: $child})",
              {"id": test_id, "child": test_id + "_child"})
    try:
        with pytest.raises(Neo4jError):
            repository.delete_person(test_id)
        assert repository.exists_by_id(test_id)
    finally:
        run_write("MATCH (p:Person {id: $id})-[:TEST_LINK]->(child) DETACH DELETE child",
                  {"id": test_id})

"""Neo4j persistence for Person nodes."""
from typing import Optional

from core.constants import PERSON_FIELDS
from core.neo4j_connection import run_read, run_write


def _person(properties: dict) -> dict:
    # Neo4j omits properties whose value is null; keep the public dict shape stable.
    return {field: properties.get(field) for field in PERSON_FIELDS}


def create_person(person: dict) -> dict:
    rows = run_write(
        "CREATE (p:Person {id: $id, full_name: $full_name, gender: $gender, "
        "birth_date: $birth_date, address: $address, phone: $phone, note: $note}) "
        "RETURN properties(p) AS person",
        person,
    )
    return _person(rows[0]["person"])


def find_by_id(person_id: str) -> Optional[dict]:
    rows = run_read("MATCH (p:Person {id: $id}) RETURN properties(p) AS person", {"id": person_id})
    return _person(rows[0]["person"]) if rows else None


def exists_by_id(person_id: str) -> bool:
    rows = run_read("MATCH (p:Person {id: $id}) RETURN count(p) > 0 AS exists", {"id": person_id})
    return rows[0]["exists"]


def find_all(skip: int = 0, limit: int = 100) -> list[dict]:
    rows = run_read(
        "MATCH (p:Person) RETURN properties(p) AS person ORDER BY p.id SKIP $skip LIMIT $limit",
        {"skip": skip, "limit": limit},
    )
    return [_person(row["person"]) for row in rows]


def search_by_keyword(keyword: str, gender: Optional[str] = None) -> list[dict]:
    rows = run_read(
        "MATCH (p:Person) WHERE ($gender IS NULL OR p.gender = $gender) "
        "AND ($keyword = '' OR toLower(p.full_name) CONTAINS toLower($keyword) "
        "OR toLower(p.id) CONTAINS toLower($keyword)) "
        "RETURN properties(p) AS person ORDER BY p.id",
        {"keyword": keyword, "gender": gender},
    )
    return [_person(row["person"]) for row in rows]


def update_person(person_id: str, changes: dict) -> Optional[dict]:
    rows = run_write(
        "MATCH (p:Person {id: $id}) SET p += $changes RETURN properties(p) AS person",
        {"id": person_id, "changes": changes},
    )
    return _person(rows[0]["person"]) if rows else None


def delete_person(person_id: str) -> bool:
    # Plain DELETE deliberately fails when the person has family relationships.
    rows = run_write(
        "MATCH (p:Person {id: $id}) WITH p, properties(p) AS person "
        "DELETE p RETURN person",
        {"id": person_id},
    )
    return bool(rows)


def count_all() -> int:
    return run_read("MATCH (p:Person) RETURN count(p) AS count")[0]["count"]


def count_by_gender() -> dict[str, int]:
    counts = {"MALE": 0, "FEMALE": 0}
    rows = run_read("MATCH (p:Person) RETURN p.gender AS gender, count(p) AS count")
    for row in rows:
        if row["gender"] in counts:
            counts[row["gender"]] = row["count"]
    return counts


def get_next_id() -> str:
    """Suggest an ID for the form; the unique constraint handles concurrent creates."""
    rows = run_read("MATCH (p:Person) WHERE p.id =~ 'P[0-9]+' RETURN p.id AS id")
    numbers = [int(row["id"][1:]) for row in rows]
    return f"P{max(numbers, default=0) + 1:03d}"

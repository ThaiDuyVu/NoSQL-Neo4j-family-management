"""Kiểm tra toàn bộ cặp kinship được cam kết trong docs/DEMO_FLOW.md."""

from collections import deque

import pytest

from database.seed_data import SAMPLE_PERSONS, SAMPLE_RELATIONSHIPS
from features.kinship.resolver import resolve_kinship
from features.relationship_search.service import build_steps_from_raw_path


PEOPLE = {
    person_id: {
        "id": person_id,
        "full_name": full_name,
        "gender": gender,
        "birth_date": birth_date,
    }
    for person_id, full_name, gender, birth_date in SAMPLE_PERSONS
}


def build_seed_path(start_id: str, target_id: str) -> dict:
    adjacency = {person_id: [] for person_id in PEOPLE}
    for from_id, to_id, rel_type in SAMPLE_RELATIONSHIPS:
        relationship = {"type": rel_type, "start_id": from_id, "end_id": to_id}
        adjacency[from_id].append((to_id, relationship))
        adjacency[to_id].append((from_id, relationship))

    queue = deque([start_id])
    previous = {start_id: None}
    while queue:
        current = queue.popleft()
        if current == target_id:
            break
        for neighbor, relationship in adjacency[current]:
            if neighbor not in previous:
                previous[neighbor] = (current, relationship)
                queue.append(neighbor)

    node_ids = []
    relationships = []
    current = target_id
    while current != start_id:
        node_ids.append(current)
        parent, relationship = previous[current]
        relationships.append(relationship)
        current = parent
    node_ids.append(start_id)
    node_ids.reverse()
    relationships.reverse()
    return {
        "nodes": [PEOPLE[person_id] for person_id in node_ids],
        "relationships": relationships,
    }


@pytest.mark.parametrize(
    ("person_a_id", "person_b_id", "expected"),
    [
        ("P011", "P004", "Cha"),
        ("P011", "P008", "Mẹ"),
        ("P011", "P001", "Ông nội"),
        ("P011", "P002", "Bà nội"),
        ("P011", "P006", "Ông ngoại"),
        ("P011", "P007", "Bà ngoại"),
        ("P011", "P012", "Em"),
        ("P012", "P011", "Anh"),
        ("P011", "P003", "Bác"),
        ("P011", "P005", "Cô"),
        ("P011", "P009", "Cậu"),
        ("P011", "P010", "Dì"),
        ("P011", "P014", "Anh họ"),
        ("P011", "P015", "Vợ"),
        ("P015", "P011", "Chồng"),
        ("P004", "P016", "Cháu"),
        ("P016", "P001", "Cụ"),
    ],
)
def test_demo_pair(person_a_id, person_b_id, expected):
    raw_path = build_seed_path(person_a_id, person_b_id)
    steps = build_steps_from_raw_path(raw_path, person_a_id)
    result = resolve_kinship(
        steps,
        PEOPLE[person_a_id]["gender"],
        PEOPLE[person_b_id]["gender"],
    )
    assert result.a_calls_b == expected

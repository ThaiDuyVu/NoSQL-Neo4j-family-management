"""Unit tests cho logic xưng hô, không cần Neo4j."""

import pytest

from features.kinship.resolver import PathStep, classify_path, compare_age, resolve_kinship


def person(person_id, gender, birth_date, name=""):
    return {"id": person_id, "gender": gender, "birth_date": birth_date, "name": name}


def path(nodes, edges):
    return [
        PathStep(
            from_id=nodes[index]["id"],
            to_id=nodes[index + 1]["id"],
            rel_type=rel_type,
            direction=direction,
            from_gender=nodes[index]["gender"],
            to_gender=nodes[index + 1]["gender"],
            from_birth_date=nodes[index]["birth_date"],
            to_birth_date=nodes[index + 1]["birth_date"],
            from_name=nodes[index]["name"],
            to_name=nodes[index + 1]["name"],
        )
        for index, (rel_type, direction) in enumerate(edges)
    ]


PHUC = person("P011", "MALE", "1995-01-01", "Phúc")
DUNG = person("P004", "MALE", "1968-01-01", "Dũng")
MAI = person("P008", "FEMALE", "1970-01-01", "Mai")
AN = person("P001", "MALE", "1940-01-01", "An")
BINH = person("P002", "FEMALE", "1943-01-01", "Bình")


@pytest.mark.parametrize(
    ("steps", "a_gender", "b_gender", "a_calls_b", "b_calls_a"),
    [
        (path([PHUC, DUNG], [("FATHER_OF", "UP")]), "MALE", "MALE", "Cha", "Con trai"),
        (path([PHUC, MAI], [("MOTHER_OF", "UP")]), "MALE", "FEMALE", "Mẹ", "Con trai"),
        (
            path([person("D", "FEMALE", "2020-01-01"), MAI], [("MOTHER_OF", "UP")]),
            "FEMALE", "FEMALE", "Mẹ", "Con gái",
        ),
        (
            path([PHUC, DUNG, AN], [("FATHER_OF", "UP"), ("FATHER_OF", "UP")]),
            "MALE", "MALE", "Ông nội", "Cháu",
        ),
        (
            path([PHUC, MAI, BINH], [("MOTHER_OF", "UP"), ("MOTHER_OF", "UP")]),
            "MALE", "FEMALE", "Bà ngoại", "Cháu",
        ),
        (
            path(
                [PHUC, DUNG, person("P012", "FEMALE", "1998-01-01", "Quỳnh")],
                [("FATHER_OF", "UP"), ("FATHER_OF", "DOWN")],
            ),
            "MALE", "FEMALE", "Em", "Anh",
        ),
        (
            path(
                [PHUC, DUNG, AN, person("P003", "MALE", "1965-01-01"), person("P014", "MALE", "1993-01-01")],
                [
                    ("FATHER_OF", "UP"), ("FATHER_OF", "UP"),
                    ("FATHER_OF", "DOWN"), ("FATHER_OF", "DOWN"),
                ],
            ),
            "MALE", "MALE", "Anh họ", "Em họ",
        ),
        (
            path([PHUC, DUNG, AN, person("P003", "MALE", "1965-01-01")], [
                ("FATHER_OF", "UP"), ("FATHER_OF", "UP"), ("FATHER_OF", "DOWN")
            ]),
            "MALE", "MALE", "Bác", "Cháu",
        ),
        (
            path([PHUC, DUNG, AN, person("P005", "FEMALE", "1971-01-01")], [
                ("FATHER_OF", "UP"), ("FATHER_OF", "UP"), ("FATHER_OF", "DOWN")
            ]),
            "MALE", "FEMALE", "Cô", "Cháu",
        ),
        (
            path([PHUC, MAI, person("P006", "MALE", "1942-01-01"), person("P009", "MALE", "1973-01-01")], [
                ("MOTHER_OF", "UP"), ("FATHER_OF", "UP"), ("FATHER_OF", "DOWN")
            ]),
            "MALE", "MALE", "Cậu", "Cháu",
        ),
        (
            path([PHUC, MAI, person("P006", "MALE", "1942-01-01"), person("P010", "FEMALE", "1976-01-01")], [
                ("MOTHER_OF", "UP"), ("FATHER_OF", "UP"), ("FATHER_OF", "DOWN")
            ]),
            "MALE", "FEMALE", "Dì", "Cháu",
        ),
        (
            path([PHUC, person("P015", "FEMALE", "1996-01-01", "Uyên")], [("SPOUSE_OF", "SPOUSE")]),
            "MALE", "FEMALE", "Vợ", "Chồng",
        ),
        (
            path([DUNG, PHUC, person("P016", "MALE", "2022-01-01")], [
                ("FATHER_OF", "DOWN"), ("FATHER_OF", "DOWN")
            ]),
            "MALE", "MALE", "Cháu", "Ông nội",
        ),
        (
            path([person("P016", "MALE", "2022-01-01"), PHUC, DUNG, AN], [
                ("FATHER_OF", "UP"), ("FATHER_OF", "UP"), ("FATHER_OF", "UP")
            ]),
            "MALE", "MALE", "Cụ", "Cháu",
        ),
    ],
)
def test_resolve_supported_terms(steps, a_gender, b_gender, a_calls_b, b_calls_a):
    result = resolve_kinship(steps, a_gender, b_gender)
    assert result.found is True
    assert result.a_calls_b == a_calls_b
    assert result.b_calls_a == b_calls_a


def test_classify_path():
    steps = path([PHUC, DUNG, AN], [("FATHER_OF", "UP"), ("FATHER_OF", "UP")])
    assert classify_path(steps) == "UP,UP"


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("1990-01-01", "2000-01-01", -1),
        ("2000-01-01", "1990-01-01", 1),
        ("2000-01-01", "2000-01-01", 0),
        (None, "2000-01-01", 0),
        ("không-hợp-lệ", "2000-01-01", 0),
    ],
)
def test_compare_age(a, b, expected):
    assert compare_age(a, b) == expected


def test_resolve_same_person():
    result = resolve_kinship([], "MALE", "MALE")
    assert result.found is False
    assert "đường đi rỗng" in result.message


def test_resolve_missing_birth_date_uses_neutral_term():
    unknown = person("A", "MALE", None)
    sibling = person("B", "FEMALE", None)
    parent = person("P", "MALE", "1970-01-01")
    result = resolve_kinship(
        path([unknown, parent, sibling], [("FATHER_OF", "UP"), ("FATHER_OF", "DOWN")]),
        "MALE",
        "FEMALE",
    )
    assert result.a_calls_b == "Anh/chị/em"
    assert result.b_calls_a == "Anh/chị/em"


def test_resolve_unsupported_path_keeps_found_path():
    steps = path(
        [PHUC, person("S", "FEMALE", "1996-01-01"), person("X", "MALE", "1960-01-01")],
        [("SPOUSE_OF", "SPOUSE"), ("FATHER_OF", "UP")],
    )
    result = resolve_kinship(steps, "MALE", "MALE")
    assert result.found is True
    assert result.a_calls_b == "Chưa xác định"
    assert "chưa hỗ trợ" in result.message

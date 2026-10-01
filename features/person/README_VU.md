# README_VU — Feature `person`

**Owner:** Vũ  |  **Domain:** Person management

## Phạm vi
CRUD Person, tìm kiếm, xem chi tiết, validation Person.

## File
| File | Vai trò |
|------|---------|
| `page.py` | UI Streamlit, chỉ gọi `service` |
| `service.py` | business logic + validation + **public interface** cho Sơn/Đạt |
| `repository.py` | toàn bộ Cypher của node `:Person` |
| `model.py` | dataclass `Person` |

## Luồng
`page.py` → `service.py` → `repository.py` → `core/neo4j_connection.py` → Neo4j

## Public interface (người khác đang phụ thuộc — đừng đổi signature khi chưa báo)
- `list_persons(skip, limit)`
- `get_person(person_id)`
- `search_persons(keyword, gender)`

## Quy tắc
- Không viết Cypher trong `page.py`.
- Không đặt query Relationship trong `repository.py` của Person.
- Người khác chỉ gọi `service.py`, không import `repository.py`.

## Test
```bash
pytest tests/person -v
```

Chi tiết task: xem `docs/MEMBER_VU.md`.

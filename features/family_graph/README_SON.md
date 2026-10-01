# README_SON — Feature `family_graph`

**Owner:** Sơn  |  **Domain:** Family graph visualization

## Phạm vi
Vẽ graph quan hệ gia đình (pyvis đã có trong `requirements.txt`, có thể đổi thư viện).

## File
| File | Vai trò |
|------|---------|
| `page.py` | UI, chỉ gọi `service` |
| `service.py` | build dữ liệu nodes/edges + render HTML |

Không có repository riêng: dữ liệu lấy qua `features.relationship.service.get_graph_edges`
(Cypher nằm trong `features/relationship/repository.py`, cùng domain Sơn).

## Test
```bash
pytest tests/relationship -v   # test graph gom chung (test_family_graph_service.py)
```

Chi tiết task: xem `docs/MEMBER_SON.md`.

# README_VU — Feature `dashboard`

**Owner:** Vũ  |  **Domain:** Dashboard

## Phạm vi
Thống kê tổng số người, số nam / nữ.

## File
| File | Vai trò |
|------|---------|
| `page.py` | UI, chỉ gọi `service` |
| `service.py` | tổng hợp số liệu, lấy từ `features.person.service.get_statistics()` |

Dashboard **không có repository riêng**: query đếm nằm ở `features/person/repository.py`
(`count_all`, `count_by_gender`) và được expose qua `person.service.get_statistics()`.
Database trống hiển thị `0` ở cả ba chỉ số; lỗi kết nối được báo trên trang.

## Test
```bash
pytest tests/person -v   # test dashboard gom chung vào tests/person (file test_dashboard_service.py)
```

Chi tiết task: xem `docs/MEMBER_VU.md`.

# DEMO FLOW

Chuẩn bị:
```bash
docker compose up -d
python -m database.seed_data --reset
streamlit run app.py
```

| # | Trang | Người trình bày | Thao tác | Kết quả mong đợi |
|---|-------|-----------------|----------|------------------|
| 1 | Dashboard | Vũ | Mở Dashboard | Tổng 16 người; 8 nam / 8 nữ (với dữ liệu seed gốc) |
| 2 | Person | Vũ | Thêm Person `P017`, tìm kiếm, sửa, xem chi tiết, xóa | CRUD hoạt động, validation báo lỗi khi nhập sai |
| 3 | Relationship | Sơn | Thêm `FATHER_OF` từ người nam; thử thêm cha là người nữ / thêm cha thứ 2 / tạo vòng lặp | Thành công với case hợp lệ; case sai bị chặn với thông báo rõ |
| 4 | Family Graph | Sơn | Chọn Phúc (`P011`), độ sâu 2 | Hiển thị bố mẹ, anh chị em, ông bà, vợ, con |
| 5 | Kinship Search | Đạt | Chọn các cặp A → B bên dưới | Cách xưng hô + đường đi |

## Cặp kinship gợi ý (dữ liệu seed) — kết quả mong đợi: *A gọi B là ...*

| A | B | A gọi B là | Ghi chú |
|---|---|-----------|---------|
| Phúc (P011) | Dũng (P004) | Cha | |
| Phúc (P011) | Mai (P008) | Mẹ | |
| Phúc (P011) | An (P001) | Ông nội | |
| Phúc (P011) | Bình (P002) | Bà nội | |
| Phúc (P011) | Khoa (P006) | Ông ngoại | |
| Phúc (P011) | Lan (P007) | Bà ngoại | |
| Phúc (P011) | Quỳnh (P012) | Em | Quỳnh sinh sau |
| Quỳnh (P012) | Phúc (P011) | Anh | Phúc sinh trước |
| Phúc (P011) | Cường (P003) | Bác | anh của bố |
| Phúc (P011) | Hoa (P005) | Cô | em gái của bố |
| Phúc (P011) | Nam (P009) | Cậu | em trai của mẹ |
| Phúc (P011) | Oanh (P010) | Dì | em gái của mẹ |
| Phúc (P011) | Thành (P014) | Anh họ | con của bác |
| Phúc (P011) | Uyên (P015) | Vợ | |
| Uyên (P015) | Phúc (P011) | Chồng | |
| Dũng (P004) | Vinh (P016) | Cháu | cháu nội |
| Vinh (P016) | An (P001) | Cụ | cố nội |

Bảng này chỉ là gợi ý để demo/test; Đạt có thể điều chỉnh khi chốt quy ước (ví dụ cách gọi khi thiếu ngày sinh).

## Kịch bản ngoại lệ nên demo
- Chọn A == B
- Hai người không có quan hệ (tự tạo `P017` không nối với ai)
- Neo4j tắt → sidebar báo lỗi, page không crash

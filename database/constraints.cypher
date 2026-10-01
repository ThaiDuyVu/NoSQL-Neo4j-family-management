// ============================================================
// SHARED FILE - CẢ NHÓM
// Chạy bằng:  python -m database.seed_data --init
// Mỗi câu lệnh kết thúc bằng dấu ';'. Dòng bắt đầu bằng '//' là comment.
// ============================================================

CREATE CONSTRAINT person_id_unique IF NOT EXISTS
FOR (p:Person) REQUIRE p.id IS UNIQUE;

CREATE INDEX person_full_name_idx IF NOT EXISTS
FOR (p:Person) ON (p.full_name);

"""
============================================================
SHARED FILE - CẢ NHÓM
============================================================
Hằng số dùng chung (label, relationship type, gender).

Quy tắc:
- Hạn chế chỉnh nếu không cần.
- Không xóa code của thành viên khác.
- Thay đổi interface dùng chung phải báo nhóm.
- Không đặt business logic riêng của feature vào shared.
- Chỉ THÊM hằng số mới; không đổi tên/giá trị hằng số đang có.
============================================================
"""

# --- Node label ---
LABEL_PERSON = "Person"

# --- Relationship types (xem docs/DATA_MODEL.md) ---
REL_FATHER_OF = "FATHER_OF"   # (cha)-[:FATHER_OF]->(con)
REL_MOTHER_OF = "MOTHER_OF"   # (mẹ)-[:MOTHER_OF]->(con)
REL_SPOUSE_OF = "SPOUSE_OF"   # (chồng)-[:SPOUSE_OF]->(vợ)  (lưu 1 chiều, query vô hướng)
RELATIONSHIP_TYPES = (REL_FATHER_OF, REL_MOTHER_OF, REL_SPOUSE_OF)

# --- Gender ---
GENDER_MALE = "MALE"
GENDER_FEMALE = "FEMALE"
GENDERS = (GENDER_MALE, GENDER_FEMALE)
GENDER_LABELS_VI = {GENDER_MALE: "Nam", GENDER_FEMALE: "Nữ"}

# --- Person properties ---
PERSON_FIELDS = ("id", "full_name", "gender", "birth_date", "address", "phone", "note")

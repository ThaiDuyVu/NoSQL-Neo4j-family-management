from typing import List, Dict, Any, Optional
from features.relationship.repository import RelationshipRepository
from core import constants


def _get_rel_types() -> Dict[str, str]:
    raw = getattr(constants, "RELATIONSHIP_TYPES", ["FATHER_OF", "MOTHER_OF", "SPOUSE_OF"])
    if isinstance(raw, dict):
        return raw
    elif isinstance(raw, (tuple, list, set)):
        return {item: item for item in raw}
    return {"FATHER_OF": "FATHER_OF", "MOTHER_OF": "MOTHER_OF", "SPOUSE_OF": "SPOUSE_OF"}


RELATIONSHIP_TYPES = _get_rel_types()

# Lấy GENDER an toàn
GENDER = getattr(constants, "GENDER", getattr(constants, "GENDERS", {"MALE": "MALE", "FEMALE": "FEMALE"}))
MALE_VAL = GENDER.get("MALE", "MALE") if isinstance(GENDER, dict) else "MALE"
FEMALE_VAL = GENDER.get("FEMALE", "FEMALE") if isinstance(GENDER, dict) else "FEMALE"

# Import động PersonService từ Vũ
try:
    from features.person import service as person_service_module
    if hasattr(person_service_module, "PersonService"):
        PersonService = person_service_module.PersonService
    else:
        PersonService = None
except Exception:
    person_service_module = None
    PersonService = None


class RelationshipService:
    def __init__(self, repo: Optional[RelationshipRepository] = None, person_service: Optional[Any] = None):
        self.repo = repo or RelationshipRepository()
        if person_service:
            self.person_service = person_service
        elif PersonService:
            self.person_service = PersonService()
        else:
            self.person_service = person_service_module

    def _get_person_helper(self, person_id: str) -> Optional[Dict[str, Any]]:
        if not self.person_service:
            return {"id": person_id, "name": person_id, "gender": "UNKNOWN"}

        if hasattr(self.person_service, "get_person"):
            return self.person_service.get_person(person_id)
        elif hasattr(self.person_service, "find_person_by_id"):
            return self.person_service.find_person_by_id(person_id)
        elif callable(self.person_service):
            return self.person_service(person_id)
        
        return {"id": person_id, "name": person_id, "gender": "UNKNOWN"}

    def validate_relationship(self, source_id: str, target_id: str, rel_type: str) -> Optional[str]:
        # Rule 1: Không tự quan hệ với chính mình
        if source_id == target_id:
            return "Không thể tạo quan hệ với chính mình."

        # Rule 2: Kiểm tra sự tồn tại của Person
        source = self._get_person_helper(source_id)
        target = self._get_person_helper(target_id)
        if not source or not target:
            return "Thành viên (Person) không tồn tại trong hệ thống."

        # Rule 3: Trùng relationship
        if self.repo.relationship_exists(source_id, target_id, rel_type):
            return f"Quan hệ {rel_type} giữa hai thành viên này đã tồn tại."

        father_type = RELATIONSHIP_TYPES.get("FATHER_OF", "FATHER_OF")
        mother_type = RELATIONSHIP_TYPES.get("MOTHER_OF", "MOTHER_OF")
        spouse_type = RELATIONSHIP_TYPES.get("SPOUSE_OF", "SPOUSE_OF")

        # Rule theo loại quan hệ
        if rel_type == father_type:
            # Cha phải là Nam
            s_gender = str(source.get("gender", "")).upper()
            if s_gender and s_gender != str(MALE_VAL).upper():
                return "Cha phải có giới tính là Nam (MALE)."
            # Con tối đa 1 cha
            parents = self.repo.count_parents(target_id)
            if parents["father_count"] >= 1:
                return f"{target.get('name', target_id)} đã có cha trong hệ thống."
            # Vòng lặp tổ tiên
            if self.repo.is_ancestor(target_id, source_id):
                return "Tạo quan hệ này sẽ gây ra vòng lặp tổ tiên."

        elif rel_type == mother_type:
            # Mẹ phải là Nữ
            s_gender = str(source.get("gender", "")).upper()
            if s_gender and s_gender != str(FEMALE_VAL).upper():
                return "Mẹ phải có giới tính là Nữ (FEMALE)."
            # Con tối đa 1 mẹ
            parents = self.repo.count_parents(target_id)
            if parents["mother_count"] >= 1:
                return f"{target.get('name', target_id)} đã có mẹ trong hệ thống."
            # Vòng lặp tổ tiên
            if self.repo.is_ancestor(target_id, source_id):
                return "Tạo quan hệ này sẽ gây ra vòng lặp tổ tiên."

        elif rel_type == spouse_type:
            # Không phải cha/mẹ/con của nhau
            if self.repo.is_ancestor(source_id, target_id) or self.repo.is_ancestor(target_id, source_id):
                return "Không thể kết hôn giữa người có quan hệ cha/mẹ - con."
            # Giới hạn số vợ/chồng (tối đa 1)
            if self.repo.count_spouses(source_id) >= 1:
                return f"{source.get('name', source_id)} hiện tại đã có hôn phối."
            if self.repo.count_spouses(target_id) >= 1:
                return f"{target.get('name', target_id)} hiện tại đã có hôn phối."

        return None

    def add_relationship(self, source_id: str, target_id: str, rel_type: str) -> bool:
        error = self.validate_relationship(source_id, target_id, rel_type)
        if error:
            raise ValueError(error)
        return self.repo.create_relationship(source_id, target_id, rel_type)

    def remove_relationship(self, source_id: str, target_id: str, rel_type: str) -> bool:
        return self.repo.delete_relationship(source_id, target_id, rel_type)

    def get_relationships_of_person(self, person_id: str) -> List[Dict[str, Any]]:
        return self.repo.find_relationships_of_person(person_id)

    def list_relationships(self) -> List[Dict[str, Any]]:
        return self.repo.find_all_relationships()

    def get_graph_edges(self, root_person_id: Optional[str] = None, depth: int = 2) -> List[Dict[str, Any]]:
        return self.repo.get_graph_edges(root_person_id, depth)
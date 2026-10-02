from typing import List, Dict, Any, Optional
from core import constants


def _get_rel_types() -> Dict[str, str]:
    raw = getattr(constants, "RELATIONSHIP_TYPES", ["FATHER_OF", "MOTHER_OF", "SPOUSE_OF"])
    if isinstance(raw, dict):
        return raw
    elif isinstance(raw, (tuple, list, set)):
        return {item: item for item in raw}
    return {"FATHER_OF": "FATHER_OF", "MOTHER_OF": "MOTHER_OF", "SPOUSE_OF": "SPOUSE_OF"}


RELATIONSHIP_TYPES = _get_rel_types()


class RelationshipRepository:
    """
    Repository layer xử lý truy vấn Cypher liên quan đến Quan hệ (Relationship) giữa các Person.
    """

    def _execute(self, query: str, parameters: dict = None) -> List[Dict[str, Any]]:
        from core import neo4j_connection
        if hasattr(neo4j_connection, "run_read"):
            return neo4j_connection.run_read(query, parameters or {})
        elif hasattr(neo4j_connection, "execute_query"):
            return neo4j_connection.execute_query(query, parameters or {})
        elif hasattr(neo4j_connection, "get_db"):
            return neo4j_connection.get_db().execute_query(query, parameters or {})
        elif hasattr(neo4j_connection, "Neo4jConnection"):
            return neo4j_connection.Neo4jConnection().execute_query(query, parameters or {})
        else:
            raise NotImplementedError("Không tìm thấy hàm thực thi query trong core.neo4j_connection")

    @staticmethod
    def _validate_rel_type(rel_type: str):
        rel_dict = _get_rel_types()
        allowed = list(rel_dict.values())
        if rel_type not in allowed:
            raise ValueError(f"Relationship type không hợp lệ: {rel_type}")

    def create_relationship(self, source_id: str, target_id: str, rel_type: str) -> bool:
        self._validate_rel_type(rel_type)
        query = f"""
        MATCH (a:Person {{id: $source_id}})
        MATCH (b:Person {{id: $target_id}})
        MERGE (a)-[r:{rel_type}]->(b)
        RETURN count(r) AS created
        """
        results = self._execute(query, {"source_id": source_id, "target_id": target_id})
        if results and results[0]["created"] > 0:
            return True
        return False

    def delete_relationship(self, source_id: str, target_id: str, rel_type: str) -> bool:
        self._validate_rel_type(rel_type)
        spouse_type = RELATIONSHIP_TYPES.get("SPOUSE_OF", "SPOUSE_OF")
        if rel_type == spouse_type:
            query = """
            MATCH (a:Person {id: $source_id})-[r:SPOUSE_OF]-(b:Person {id: $target_id})
            DELETE r
            RETURN count(r) AS deleted
            """
        else:
            query = f"""
            MATCH (a:Person {{id: $source_id}})-[r:{rel_type}]->(b:Person {{id: $target_id}})
            DELETE r
            RETURN count(r) AS deleted
            """
        results = self._execute(query, {"source_id": source_id, "target_id": target_id})
        if results and results[0]["deleted"] > 0:
            return True
        return False

    def relationship_exists(self, source_id: str, target_id: str, rel_type: str) -> bool:
        self._validate_rel_type(rel_type)
        spouse_type = RELATIONSHIP_TYPES.get("SPOUSE_OF", "SPOUSE_OF")
        if rel_type == spouse_type:
            query = """
            MATCH (a:Person {id: $source_id})-[r:SPOUSE_OF]-(b:Person {id: $target_id})
            RETURN count(r) > 0 AS exists
            """
        else:
            query = f"""
            MATCH (a:Person {{id: $source_id}})-[r:{rel_type}]->(b:Person {{id: $target_id}})
            RETURN count(r) > 0 AS exists
            """
        results = self._execute(query, {"source_id": source_id, "target_id": target_id})
        return bool(results and results[0]["exists"])

    def find_relationships_of_person(self, person_id: str) -> List[Dict[str, Any]]:
        query = """
        MATCH (p:Person {id: $person_id})-[r]->(other:Person)
        RETURN p.id AS source_id, p.name AS source_name, type(r) AS rel_type, other.id AS target_id, other.name AS target_name, 'OUTGOING' AS direction
        UNION
        MATCH (other:Person)-[r]->(p:Person {id: $person_id})
        RETURN other.id AS source_id, other.name AS source_name, type(r) AS rel_type, p.id AS target_id, p.name AS target_name, 'INCOMING' AS direction
        """
        return self._execute(query, {"person_id": person_id})

    def find_all_relationships(self) -> List[Dict[str, Any]]:
        query = """
        MATCH (a:Person)-[r]->(b:Person)
        RETURN a.id AS source_id, a.name AS source_name, type(r) AS rel_type, b.id AS target_id, b.name AS target_name
        ORDER BY a.name, type(r)
        """
        return self._execute(query)

    def count_parents(self, person_id: str) -> Dict[str, int]:
        query = """
        MATCH (p:Person {id: $person_id})
        OPTIONAL MATCH (f:Person)-[:FATHER_OF]->(p)
        OPTIONAL MATCH (m:Person)-[:MOTHER_OF]->(p)
        RETURN count(DISTINCT f) AS father_count, count(DISTINCT m) AS mother_count
        """
        results = self._execute(query, {"person_id": person_id})
        if results:
            return {
                "father_count": results[0]["father_count"],
                "mother_count": results[0]["mother_count"]
            }
        return {"father_count": 0, "mother_count": 0}

    def count_spouses(self, person_id: str) -> int:
        query = """
        MATCH (p:Person {id: $person_id})-[r:SPOUSE_OF]-(s:Person)
        RETURN count(DISTINCT s) AS spouse_count
        """
        results = self._execute(query, {"person_id": person_id})
        return results[0]["spouse_count"] if results else 0

    def is_ancestor(self, possible_ancestor_id: str, person_id: str) -> bool:
        query = """
        MATCH path = (a:Person {id: $ancestor_id})-[:FATHER_OF|MOTHER_OF*1..]->(b:Person {id: $person_id})
        RETURN count(path) > 0 AS is_ancestor
        """
        results = self._execute(query, {"ancestor_id": possible_ancestor_id, "person_id": person_id})
        return bool(results and results[0]["is_ancestor"])

    def get_graph_edges(self, root_person_id: Optional[str] = None, depth: int = 2) -> List[Dict[str, Any]]:
        if root_person_id:
            query = """
            MATCH (root:Person {id: $root_id})
            MATCH path = (root)-[*1..%d]-(other:Person)
            UNWIND relationships(path) AS r
            WITH startNode(r) AS a, r, endNode(r) AS b
            RETURN DISTINCT 
                a.id AS source_id, a.name AS source_name, a.gender AS source_gender,
                type(r) AS rel_type,
                b.id AS target_id, b.name AS target_name, b.gender AS target_gender
            """ % depth
            return self._execute(query, {"root_id": root_person_id})
        else:
            query = """
            MATCH (a:Person)-[r]->(b:Person)
            RETURN 
                a.id AS source_id, a.name AS source_name, a.gender AS source_gender,
                type(r) AS rel_type,
                b.id AS target_id, b.name AS target_name, b.gender AS target_gender
            """
            return self._execute(query)
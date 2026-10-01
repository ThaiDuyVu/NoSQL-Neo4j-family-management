import pytest
from features.family_graph.service import FamilyGraphService


def test_build_graph_data(mocker):
    mock_rel_svc = mocker.Mock()
    mock_rel_svc.get_graph_edges.return_value = [
        {
            "source_id": "P1", "source_name": "Cha", "source_gender": "MALE",
            "rel_type": "FATHER_OF",
            "target_id": "P2", "target_name": "Con", "target_gender": "FEMALE"
        }
    ]

    service = FamilyGraphService(rel_service=mock_rel_svc)
    data = service.build_graph_data()

    assert len(data["nodes"]) == 2
    assert len(data["edges"]) == 1
    assert data["nodes"][0]["id"] == "P1"
    assert data["edges"][0]["from"] == "P1"
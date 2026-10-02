import json
from typing import Dict, Any, Optional
from features.relationship.service import RelationshipService


class FamilyGraphService:
    def __init__(self, rel_service: Optional[RelationshipService] = None):
        self.rel_service = rel_service or RelationshipService()

    def build_graph_data(self, root_person_id: Optional[str] = None, depth: int = 2) -> Dict[str, Any]:
        """Tạo dữ liệu nodes & edges cho pyvis / vis.js."""
        edges_data = self.rel_service.get_graph_edges(root_person_id, depth)

        nodes_dict = {}
        edges_list = []

        for item in edges_data:
            s_id = item["source_id"]
            t_id = item["target_id"]

            # Source Node
            if s_id not in nodes_dict:
                color = "#4CAF50" if item.get("source_gender") == "MALE" else "#E91E63"
                nodes_dict[s_id] = {
                    "id": s_id,
                    "label": item.get("source_name", s_id),
                    "color": color,
                    "shape": "dot",
                    "size": 20
                }

            # Target Node
            if t_id not in nodes_dict:
                color = "#4CAF50" if item.get("target_gender") == "MALE" else "#E91E63"
                nodes_dict[t_id] = {
                    "id": t_id,
                    "label": item.get("target_name", t_id),
                    "color": color,
                    "shape": "dot",
                    "size": 20
                }

            # Edge
            rel_type = item.get("rel_type")
            edge_color = "#2196F3"
            if rel_type == "SPOUSE_OF":
                edge_color = "#9C27B0"

            edges_list.append({
                "from": s_id,
                "to": t_id,
                "label": rel_type,
                "color": edge_color,
                "arrows": "to" if rel_type != "SPOUSE_OF" else ""
            })

        return {
            "nodes": list(nodes_dict.values()),
            "edges": edges_list
        }

    def render_graph_html(self, root_person_id: Optional[str] = None, depth: int = 2) -> str:
        """Tạo HTML hiển thị Đồ thị gia đình sử dụng vis.js."""
        graph_data = self.build_graph_data(root_person_id, depth)
        nodes_json = json.dumps(graph_data["nodes"])
        edges_json = json.dumps(graph_data["edges"])

        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
          <style type="text/css">
            #family-network {{
              width: 100%;
              height: 550px;
              border: 1px solid #cccccc;
              background-color: #f9f9f9;
              border-radius: 8px;
            }}
          </style>
        </head>
        <body>
        <div id="family-network"></div>
        <script type="text/javascript">
          var nodes = new vis.DataSet({nodes_json});
          var edges = new vis.DataSet({edges_json});
          var container = document.getElementById('family-network');
          var data = {{
            nodes: nodes,
            edges: edges
          }};
          var options = {{
            nodes: {{
              font: {{ size: 14, color: '#333333' }}
            }},
            edges: {{
              font: {{ size: 12, align: 'middle' }},
              smooth: {{ type: 'cubicBezier' }}
            }},
            physics: {{
              barnesHut: {{ gravConstant: -3000, springLength: 95 }}
            }}
          }};
          var network = new vis.Network(container, data, options);
        </script>
        </body>
        </html>
        """
        return html_code
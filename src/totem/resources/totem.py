from typing import Literal

from ocelescope import Resource
from ocelescope.visualization.default.graph import EdgeArrow, Graph, GraphEdge, GraphNode, GraphvizLayoutConfig
from ocelescope.visualization.util.color import generate_color_map
from pydantic import BaseModel

Temporal_Relation_Constant = Literal["D", "Di", "I", "Ii", "P"]

Cardinality = Literal["0", "1", "0...1", "1..*", "0...*"]


class TotemEdge(BaseModel):
    source: str
    target: str
    lc: Cardinality | None
    lc_inverse: Cardinality | None
    ec: Cardinality | None
    ec_inverse: Cardinality | None
    tr: Temporal_Relation_Constant | None
    tr_inverse: Temporal_Relation_Constant | None


class Totem(Resource):
    label = "Totem"
    description = "A totem graph"

    object_types: list[str]
    edges: list[TotemEdge]
    type: Literal["totem"] = "totem"

    def visualize(self) -> Graph:
        def tr_to_arrow(tr: Temporal_Relation_Constant | None) -> EdgeArrow | None:
            # Cytoscape styles:
            # P -> triangle, D -> tee, I -> circle, Ii/Di -> no arrow
            return {"P": "triangle", "D": "tee", "I": "circle", "Ii": None, "Di": None, None: None}[tr]

        def edge_label_for_forward(e: TotemEdge) -> str:
            parts = []
            if e.ec:
                parts.append(e.ec)
            if e.ec_inverse:
                parts.append(e.ec_inverse)
            return " · ".join(parts) if parts else ""

        color_map = generate_color_map(self.object_types)
        nodes: list[GraphNode] = []
        for ot in self.object_types:
            nodes.append(
                GraphNode(
                    id=ot,
                    label=ot,
                    shape="rectangle",
                    color=color_map.get(ot),
                )
            )

        edges: list[GraphEdge] = []
        for e in self.edges:
            src_arrow = tr_to_arrow(e.tr_inverse)
            tgt_arrow = tr_to_arrow(e.tr)
            label = edge_label_for_forward(e)
            color = color_map.get(e.source)

            edges.append(
                GraphEdge(
                    source=e.source,
                    target=e.target,
                    arrows=(src_arrow, tgt_arrow),
                    color=color,
                    label=label,
                )
            )

        return Graph(
            type="graph",
            nodes=nodes,
            edges=edges,
            layout_config=GraphvizLayoutConfig(
                engine="neato",
                graphAttrs={
                    "overlap": "false",
                },
                edgeAttrs={"len": 3},
            ),
        )

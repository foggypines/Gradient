from .node_base_func import BaseNodeFunction
from .node_input import NodeInput
from ...lib.utility import prepend_exclamation
from dataclasses import dataclass, field

node_name = "PointOnFace"
node_type = prepend_exclamation(node_name)

node_face_input = "_input_face"
node_point_output = "_output_point"

point_on_face = None

@dataclass
class PointOnFaceNodeFunction(BaseNodeFunction):

    face: NodeInput = field(default_factory=lambda: None)

    def __post_init__(self):
        super().__post_init__()

        if self.face is None:
            self.face = self.add_input(node_face_input, ui_element=False, required=False)

    def compute(self, sender=None, app_data=None):
        point = point_on_face(self.face)

        self.output.payload = point
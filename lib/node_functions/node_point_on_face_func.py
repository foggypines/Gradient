from .node_base_func import BaseNodeFunction
from .node_input import NodeInput
from ..utility import prepend_exclamation
from dataclasses import dataclass, field

node_name = "PointOnFace"
node_type = prepend_exclamation(node_name)

node_face_input = "_input_face"
node_u_input = "_u_input"
node_v_input = "_v_input"
node_point_output = "_output_point"

point_on_face = None

@dataclass
class PointOnFaceNodeFunction(BaseNodeFunction):

    face: NodeInput = field(default_factory=lambda: None)
    u_val: NodeInput = field(default_factory=lambda: None)
    v_val: NodeInput = field(default_factory=lambda: None)

    def __post_init__(self):
        super().__post_init__()

        if self.face is None:
            self.face = self.add_input(node_face_input, ui_element=False, required=True, ui_label="Face")

        if self.u_val is None:
            self.u_val = self.add_input(node_u_input, ui_element=False, required=True, ui_label="U Value")

        if self.v_val is None:
            self.v_val = self.add_input(node_v_input, ui_element=False, required=True, ui_label="V Value")

    def compute(self, sender=None, app_data=None):
        
        if len(self.u_val.parameter) == len(self.v_val.parameter):

            point = point_on_face(faces = self.face.parameter[0], u_vals = self.u_val.parameter, 
                                  v_vals = self.v_val.parameter, node_id = self.gui_id)

            self.output.payload = point
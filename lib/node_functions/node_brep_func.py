from .node_base_func import BaseNodeFunction
from .node_output import NodeOutput
from .node_input import NodeInput
from ...lib.utility import prepend_exclamation
from dataclasses import dataclass, field

node_name = "BReP"
node_type = prepend_exclamation(node_name)
node_faces_output = "_OutputFaces"
node_bounding_box_output = "_OutputBoundingBox"
node_brep_input = "_input_brep"
node_out_put = "_Output"

@dataclass
class BRePNodeFunction(BaseNodeFunction):

    brep_input: NodeInput = field(default_factory=lambda: None)

    faces: NodeOutput = field(default_factory=lambda: None)
    bounding_box: NodeOutput = field(default_factory=lambda: None)

    def __post_init__(self):
        super().__post_init__()

        self.output.ui_label = "Physical Properties"

        if self.brep_input is None:
            self.brep_input = self.add_input(node_brep_input, ui_element=False, required=True, ui_label="BReP")

        if self.faces is None:
            self.faces = self.add_output(node_faces_output, 'Faces')

        self.outputs.append(self.faces)
        
        if self.bounding_box is None:
            self.bounding_box = self.add_output(node_bounding_box_output, 'Bounding Box')

        self.outputs.append(self.bounding_box)

    def compute(self, sender=None, app_data=None):

        brep = self.brep_input.parameter[0]

        self.output.payload = brep.physicalProperties

        self.faces.payload = brep.faces

        self.bounding_box.payload = brep.orientedMinimumBoundingBox


from .node_base_func import BaseNodeFunction
from .node_input import NodeInput
from ..utility import prepend_exclamation
from dataclasses import dataclass, field

node_type = prepend_exclamation("Transform")

brep_input = "_brep_input"

transform_bodies = None

@dataclass
class TransformNodeFunction(BaseNodeFunction):

    brep_input: NodeInput = field(default_factory=lambda: None)

    def __post_init__(self):

        super().__post_init__()

        if self.brep_input is None:

            self.brep_input = self.add_input(input_name = brep_input, ui_label = "BReP")

    def compute(self, sender=None, app_data=None):

        transform_bodies(self.brep_input.parameter[0], self.gui_id)

        self.output.payload = self.gui_id

    def delete(self):

        transform_bodies(self.node_a_input.parameter[0], self.node_b_input.parameter[0], self.gui_id, delete = True)
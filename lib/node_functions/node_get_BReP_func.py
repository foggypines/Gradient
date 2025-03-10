from .node_base_func import BaseNodeFunction
from .node_input import NodeInput
from ...lib.utility import prepend_exclamation
from dataclasses import dataclass, field

node_name = "GetBRep"
node_type = prepend_exclamation(node_name)

node_brep_input = "_input_brep"

get_brep = None

@dataclass
class GetBRepNodeFunction(BaseNodeFunction):

    brep: NodeInput = field(default_factory=lambda: None)

    def __post_init__(self):
        super().__post_init__()

        if self.brep is None:
            self.brep = self.add_input(node_brep_input, ui_element=False, required=False)

    def compute(self, sender=None, app_data=None):

        get_brep(self.gui_id)

        self.output.payload = self.gui_id
from . node_base_func import BaseNodeFunction
from . node_input import NodeInput, all_node_inputs
from ... lib.utility import prepend_exclamation, append_value
from ... lib.fusionAddInUtils.general_utils import log
from dataclasses import dataclass, field
from ... lib.enums import *

node_name = "BRepBox"
node_type = prepend_exclamation(node_name)

node_bounding_box = "_bounding_box"

node_out_put = "_Output"

make_box = None

@dataclass
class BRePBoxNodeFunction(BaseNodeFunction):

    bounding_box: NodeInput = field(default_factory=lambda: None)

    def __post_init__(self):

        super().__post_init__()

        if self.bounding_box is None:

            self.bounding_box = self.add_input(node_bounding_box)

            self.bounding_box.required = False #just for testing

    def compute(self, sender=None, app_data=None):

        for bounding_box in self.bounding_box.parameter:

            make_box(node_id=self.gui_id, bounding_box=bounding_box)

        make_box(self.gui_id, compute = True)

        self.output.payload = self.gui_id

    def delete(self):

        make_box(self.gui_id, compute = True, delete = True)
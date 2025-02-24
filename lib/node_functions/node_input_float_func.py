import dearpygui.dearpygui as dpg
from . node_base_func import BaseNodeFunction
from .node_input import NodeInput
from .node_output import NodeOutput
from ... lib.utility import append_value
from ... lib.fusionAddInUtils.general_utils import log
from dataclasses import dataclass, field

node_output = "_Output"
node_name = "NodeInputFloat"

@dataclass(kw_only=True)
class InputFloatNodeFunction(BaseNodeFunction):

    # inputs: list[NodeInput] = field(init = False, repr = False, default_factory = lambda: [])
    # outputs: list[NodeOutput] = field(init = False, repr = False, default_factory = lambda: [])
    value: float = field(default=0)

    def __post_init__(self):
        
        super().__post_init__()

    def compute(self, sender=None, app_data=None):

        self.value = dpg.get_value(append_value(self.gui_id + node_output))

        self.output.payload = self.value

        # for link in self.links:

        #     node_input = all_node_inputs[link.end]

        #     node_input.update(self.value)

        # self.broadcast_changes()
import dearpygui.dearpygui as dpg
import numpy as np
from . node_base_func import BaseNodeFunction
from . node_input import NodeInput, all_node_inputs
from ... lib.utility import append_value
from dataclasses import dataclass, field
from ... lib.fusionAddInUtils.general_utils import log

node_name = "NodeReadout"
node_input = "_Input"
node_output = "_Output"

@dataclass
class ReadoutNodeFunction(BaseNodeFunction):

    input: NodeInput = field(default = None)

    def __post_init__(self):

        if self.input is None:

            self.input = self.add_input(node_input)

    def compute(self, sender=None, app_data=None):

        rounded = np.round(self.input.parameter, decimals = 4)

        print_out = str(rounded)

        dpg.set_value(append_value(self.gui_id + "_Input"), print_out)

        for link in self.links:

            node_input = all_node_inputs[link.end]

            node_input.update(self.input.parameter) #pass the parameter through

        if sender is not None:

            self.update()
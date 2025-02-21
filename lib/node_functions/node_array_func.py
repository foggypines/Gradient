import numpy as np
from . node_base_func import BaseNodeFunction
from .node_input import NodeInput, all_node_inputs
from ... lib.utility import append_value
from ... lib.fusionAddInUtils.general_utils import log
from dataclasses import dataclass, field

node_name = "NodeArrayInput"
node_output = "_Output"
node_count = "_Count"
node_increment = "_Increment"
node_start = "_Start"

@dataclass
class ArrayNodeFunction(BaseNodeFunction):

    count: NodeInput = field(default = None)
    increment: NodeInput = field(default = None)
    start: NodeInput = field(default = None)
    array: np.float64 = field(default_factory = lambda: np.zeros((1,1), np.float64))

    def __post_init__(self):

        if self.count is None:

            self.count = self.add_input(node_count, ui_element=True)

        if self.increment is None:

            self.increment = self.add_input(node_increment, ui_element=True)

        if self.start is None:

            self.start = self.add_input(node_start, ui_element=True)

    def compute(self, sender=None, app_data=None):

        _count = self.count.parameter[0]
        _increment = self.increment.parameter[0]
        _start = self.start.parameter[0]

        _count = self.parameter_update(self.count, node_count, _count)
        _increment = self.parameter_update(self.increment, node_increment, _increment)
        _start = self.parameter_update(self.start, node_start, _start)

        _count = int(_count)

        if _increment == 0:

            self.array = np.linspace(start = _start, stop = _start, num = _count)
            
        else:

            self.array = np.linspace(start = _start, stop = _start + _count * _increment - 1, num = _count)

        for link in self.links:

            node_input = all_node_inputs[link.end]

            node_input.update(self.array)

        if sender is not None: #Detect an update triggered from the UI.

            self.broadcast_changes()
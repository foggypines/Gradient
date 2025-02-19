import dearpygui.dearpygui as dpg
from . node_base_func import BaseNodeFunction
from .node_input import NodeInput, all_node_inputs
from ... lib.fusionAddInUtils.general_utils import log
import numpy as np
from dataclasses import dataclass, field

node_output = "_Output"
node_count = "_Count"
node_min = "_Min"
node_max = "_Max"
node_set = "_Set"
node_name = "NodeArrayRandom"

@dataclass(kw_only=True)
class ArrayRandomNodeFunction(BaseNodeFunction):

    count: NodeInput = field(default = None)
    min: NodeInput = field(default = None)
    max: NodeInput = field(default = None)
    set: NodeInput = field(default = None)
    array: np.float64 = field(default_factory = lambda: np.zeros((1,1), np.float64))

    def __post_init__(self):

        if self.count is None:

            self.count = self.add_input(node_count)
            self.count.parameter[0] = 1

        if self.min is None:

            self.min = self.add_input(node_min)
            self.min.parameter[0] = 0

        if self.max is None:

            self.max = self.add_input(node_max)
            self.max.parameter[0] = 9

        if self.set is None:

            self.set = self.add_input(node_set)
            self.set.parameter[0] = 1

        # all_node_inputs[self.gui_id + node_count] = self.count
        # all_node_inputs[self.gui_id + node_min] = self.min
        # all_node_inputs[self.gui_id + node_max] = self.max
        # all_node_inputs[self.gui_id + node_set] = self.set

    def compute(self, sender=None, app_data=None):

        _count = self.count.parameter[0]
        _min = self.min.parameter[0]
        _max = self.max.parameter[0]
        _set = self.set.parameter[0]

        _count = self.parameter_update(self.count, node_count, _count)
        _min = self.parameter_update(self.min, node_min, _min)
        _max = self.parameter_update(self.max, node_max, _max)
        _set = self.parameter_update(self.set, node_set, _set)

        self.array = np.random.uniform(_min, _max, size = ((_count, _set)))

        if _set == 1: #this lets the value still be used as a 1D list

            self.array = np.random.uniform(_min, _max, _count)

        for link in self.links:

            node_input = all_node_inputs[link.end]

            node_input.update(self.array)

        if sender is not None: #Detect an update triggered from the UI.

            self.update()
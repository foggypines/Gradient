import numpy as np
from .node_base_func import BaseNodeFunction
from .node_input import NodeInput, all_node_inputs
from ... lib.utility import prepend_exclamation, append_value
from ... lib.fusionAddInUtils.general_utils import log
from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard

node_name = "Point"
node_type = prepend_exclamation(node_name)
node_x_input = "_input_x"
node_y_input = "_input_y"
node_z_input = "_input_z"

node_out_put = "_Output"

@dataclass(kw_only=True)
class PointNodeFunction(BaseNodeFunction, JSONWizard):

    x: NodeInput = field(default = None)
    y: NodeInput = field(default = None)
    z: NodeInput = field(default = None)
    points: np.float64 = field(default_factory=lambda: np.zeros((1,3), np.float64))

    def __post_init__(self):

        if self.x == None:

            self.x = NodeInput(self.gui_id)

        if self.y == None:

            self.y = NodeInput(self.gui_id)

        if self.z == None:

            self.z = NodeInput(self.gui_id)

        all_node_inputs[self.gui_id + node_x_input] = self.x
        all_node_inputs[self.gui_id + node_y_input] = self.y
        all_node_inputs[self.gui_id + node_z_input] = self.z


    def compute(self, sender=None, app_data=None):

        log('beginning compute for point funct')

        log(f"x parameter length {len(self.x.parameter)}")
        log(f"y parameter length {len(self.y.parameter)}")
        log(f"z parameter length {len(self.z.parameter)}")

        num_points = len(self.x.parameter) * len(self.y.parameter) * len(self.z.parameter)

        self.points = np.zeros((num_points, 3), np.float64)

        i = 0

        log("starting the point calculation")

        log(f"x input: {self.x.parameter}")
        log(f"y input: {self.y.parameter}")
        log(f"z input: {self.z.parameter}")

        for x in self.x.parameter:
            for y in self.y.parameter:
                for z in self.z.parameter:

                    x = self.parameter_update(self.x, node_x_input, x)
                    y = self.parameter_update(self.y, node_y_input, y)
                    z = self.parameter_update(self.z, node_z_input, z)

                    self.points[i] = np.array([x,y,z], np.float64)
                    
                    log(f"Points value: ({self.points})")
                    
                    i = i + 1

        output_len = len(self.outputs)

        link_len = len(self.links)

        log(f"{output_len} outputs for point node")
        log(f"{link_len} links for point node ")

        for link in self.links:

            log(f'link stop: {link.end}')

            node_input = all_node_inputs[link.end]

            node_input.update(self.points)

        log(f"all point links updated")

        if sender is not None:

            self.update()

    def sync_ui(self):
    
        self.set_ui(self.x, node_x_input)
        self.set_ui(self.y, node_y_input)
        self.set_ui(self.z, node_z_input)
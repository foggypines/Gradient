import numpy as np
from .node_base_func import BaseNodeFunction
from .node_input import NodeInput
from ... lib.utility import prepend_exclamation, append_value
from ... lib.fusionAddInUtils.general_utils import log
from dataclasses import dataclass, field

node_name = "Point"
node_type = prepend_exclamation(node_name)
node_x_input = "_input_x"
node_y_input = "_input_y"
node_z_input = "_input_z"

node_out_put = "_Output"

@dataclass
class MatrixNodeFunction(BaseNodeFunction):

#todo make this a matrix class 

    x: NodeInput = field(default = None)
    y: NodeInput = field(default = None)
    z: NodeInput = field(default = None)
    points: np.float64 = field(default_factory=lambda: np.zeros((1,3), np.float64))

    def __post_init__(self):

        super().__post_init__()

        if self.x == None:

            self.x = self.add_input(node_x_input, ui_element=True)

        if self.y == None:

            self.y = self.add_input(node_y_input, ui_element=True)

        if self.z == None:

            self.z = self.add_input(node_z_input, ui_element=True)

    def compute(self, sender=None, app_data=None):

        num_points = len(self.x.parameter) * len(self.y.parameter) * len(self.z.parameter)

        self.points = np.zeros((num_points, 3), np.float64)

        i = 0

        for x in self.x.parameter:
            for y in self.y.parameter:
                for z in self.z.parameter:

                    x = self.parameter_update(self.x, node_x_input, x)
                    y = self.parameter_update(self.y, node_y_input, y)
                    z = self.parameter_update(self.z, node_z_input, z)

                    self.points[i] = np.array([x,y,z], np.float64)
                                        
                    i = i + 1

        self.output.payload = self.points
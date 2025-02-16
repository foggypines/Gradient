from . node_base_func import BaseNodeFunction
from . node_input import NodeInput, all_node_inputs
from ... lib.utility import prepend_exclamation, append_value
from ... lib.fusionAddInUtils.general_utils import log
from dataclasses import dataclass, field

node_name = "Sphere"
node_type = prepend_exclamation(node_name)

node_x_input = "_input_x"
node_y_input = "_input_y"
node_z_input = "_input_z"
node_point_input = "_input_point"
node_rad_input ="_input_radius"

node_out_put = "_Output"

make_sphere = None

@dataclass
class SphereNodeFunction(BaseNodeFunction):

    point: NodeInput = field(default_factory=lambda: None)
    rad: NodeInput = field(default_factory=lambda: None)

    def __post_init__(self):

        if self.point is None:

            self.point = NodeInput(self.gui_id)

        if self.rad is None:
            
            self.rad = NodeInput(self.rad)

            self.rad.parameter[0] = 1

        all_node_inputs[self.gui_id + node_point_input] = self.point
        all_node_inputs[self.gui_id + node_rad_input] = self.rad

    def compute(self, sender=None, app_data=None):

        log('begin sphere compute')

        i = 0

        log(f"Sphere point input:     ({self.point.parameter})")
        log(f"Spher Radius input:     ({self.rad.parameter})")

        for point in self.point.parameter:

            rad = self.rad.parameter[i]

            rad = self.parameter_update(self.rad, node_rad_input, rad)

            log('Sphere value: ')
            
            log(f"  position: ({point[0]},{point[1]},{point[2]}")
            log(f"  radius: {rad}")

            make_sphere(point[0],point[1],point[2], rad, self.gui_id)

            if i == len(self.rad.parameter) - 1:
                i = 0
            else:
                i = i + 1

        make_sphere(0,0,0, 0, self.gui_id, True)

        for link in self.links:

            node_input = all_node_inputs[link.end]

            node_input.update(self.gui_id)
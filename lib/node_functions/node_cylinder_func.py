from . node_base_func import BaseNodeFunction
from . node_input import NodeInput, all_node_inputs
from ... lib.utility import prepend_exclamation, append_value
from ... lib.fusionAddInUtils.general_utils import log
from dataclasses import dataclass, field

node_name = "Cylinder"
node_type = prepend_exclamation(node_name)

node_point_input ="_input_point"
node_vector_input = "_input_vector"
node_radius_input = "_input_radius"
node_output = "_Output"

make_cylinder = None

@dataclass
class CylinderNodeFunction(BaseNodeFunction):

    point: NodeInput = field(default_factory=lambda: None)
    vector: NodeInput = field(default_factory=lambda: None)
    rad: NodeInput = field(default_factory=lambda: None)

    def __post_init__(self):

        if self.point is None:

            self.point = self.add_input(node_point_input)

        if self.vector is None:
            
            self.vector = self.add_input(node_vector_input)

        if self.rad is None:

            self.rad = self.add_input(node_radius_input, ui_element=True)

            self.rad.parameter[0] = 1 #default to 1 to avoid zero val radius

    def compute(self, sender=None, app_data=None):

        i = 0

        if len(self.point.parameter) == len(self.vector.parameter):
            
            j = 0

            for i in range(0, len(self.point.parameter)):

                point = self.point.parameter[i]

                vector = self.vector.parameter[i]

                rad = self.rad.parameter[j]

                rad = self.parameter_update(self.rad, node_radius_input, rad)

                make_cylinder(point, vector, rad, self.gui_id)

                if j == len(self.rad.parameter) - 1:
                    j = 0
                else:
                    j = j + 1
        else: 

            log("Point and vector input mismatch cylinder not computed!")

        make_cylinder([0,0,0], [0,0,0], 0, self.gui_id, True)

        for link in self.links:

            node_input = all_node_inputs[link.end]

            node_input.update(self.points)

        if sender is not None:

            self.broadcast_changes()
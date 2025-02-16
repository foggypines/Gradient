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

            self.point = NodeInput(self.gui_id)

        if self.vector is None:
            
            self.vector = NodeInput(self.gui_id)

        if self.rad is None:

            self.rad = NodeInput(self.gui_id)

            self.rad.parameter[0] = 1 #default to 1 to avoid zero val radius

        all_node_inputs[self.gui_id + node_point_input] = self.point
    
        all_node_inputs[self.gui_id + node_vector_input] = self.vector
        
        all_node_inputs[self.gui_id + node_radius_input] = self.rad

    def compute(self, sender=None, app_data=None):

        log('begin Cylinder compute')

        i = 0

        log(f"Point len {len(self.point.parameter)}")
        log(f"Vector len {len(self.vector.parameter)}")

        if len(self.point.parameter) == len(self.vector.parameter):

            log("parameter length passed")
            
            j = 0

            for i in range(0, len(self.point.parameter)):

                log("made it here")

                point = self.point.parameter[i]

                log("got point")

                vector = self.vector.parameter[i]

                log("got vector")

                rad = self.rad.parameter[j]

                log("got radius part 1")

                rad = self.parameter_update(self.rad, node_radius_input, rad)

                log("got parameters")

                log('Cylinder value: ')
                
                log(f"  position: ({point[0]},{point[1]},{point[2]})")
                log(f"  vector:   ({vector[0]},{vector[1]},{vector[2]})")
                log(f"  radius:   {rad}")

                make_cylinder(point, vector, rad, self.gui_id)

                if j == len(self.rad.parameter) - 1:
                    j = 0
                else:
                    j = j + 1
        else: 

            log("Point and vector input mismatch cylinder not computed!")


        make_cylinder([0,0,0], [0,0,0], 0, self.gui_id, True)
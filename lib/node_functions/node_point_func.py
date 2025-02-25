import numpy as np
# from .node_base_func import BaseNodeFunction
from .node_three_dim_func import ThreeDimNodeFunction
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
class PointNodeFunction(ThreeDimNodeFunction, JSONWizard):
    '''Point Node Function Class'''
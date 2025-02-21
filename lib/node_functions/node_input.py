from ... lib.fusionAddInUtils.general_utils import log
import numpy as np
from dataclasses import dataclass, field

all_node_inputs = {}

@dataclass
class NodeInput():

    gui_id: str
    parameter: np.float64 = field(default_factory=lambda: np.array([0], np.float64))
    linked: bool = False
    
    #indicates if the node input has a control element that can be used in place of a link to another node
    ui_element: bool = False 

    def __post__init__(self):

        self.update(self.parameter)

    def update(self, parameter):

        if isinstance(parameter, list) or isinstance(parameter, np.ndarray):  

            self.parameter = parameter

        else:

            self.parameter = [parameter]